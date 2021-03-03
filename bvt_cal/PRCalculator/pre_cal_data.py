#!/usr/bin/python
# -*- coding:utf-8 -*-

import hashlib
import pandas as pd
import re
import codecs
import json

find_dict = {'tianqi_100-1362964723065118720': 'general_search', 'shoudu_100-1363009765788008448': 'search_capital', 'xinwen_100-1362971025342423040': 'search_news',
             'jibing_100-1362963779678068736': 'qa_firstaid_treatment', 'huangli_100-1362948838480896000': 'search_almanac'}


def select_data(filename):
    data = pd.read_csv(filename, encoding='utf-8')
    data['true_slots'] = data['人工标注'].apply(lambda x: context2slots(x))
    data['pred_slots'] = data['平台标注'].apply(lambda x: context2slots(x))
    data['corpus_id'] = data['语料'].apply(lambda x: hashlib.md5(x.encode(encoding='UTF-8')).hexdigest())
    res = data[['corpus_id', '语料', '平台领域', '平台意图', 'pred_slots', '人工领域', '人工意图', 'true_slots']].copy()
    res = res.rename(columns={'corpus_id': 'corpus_id', '语料': 'corpus_context', '平台领域': 'pred_domain_name', '平台意图': 'pred_intent_name',
                     'pred_slots': 'pred_slots', '人工领域': 'true_domain_name', '人工意图': 'true_intent_name', 'true_slots': 'true_slots'})
    res['domain_intent'] = res['true_domain_name'] + '|' + res['true_intent_name']
    res.to_excel('select_data_100.xlsx', encoding='utf-8')
    return res


def context2slots(contexts):
    pattern = r'<(.+?)>(.+?)<'
    result = []
    res = re.findall(pattern, contexts)
    if res:
        for name in res:
            res_dic = dict()
            res_dic[name[0]] = name[1]
            result.append(res_dic)
        result = dic_in_list_sorted(result)
    return result


def merge_pt_out(online=None, offline=None):
    merge_data = online.copy()
    assert len(online) == len(offline), 'online = {}, offline = {}'.format(len(online), len(offline))
    online['pile'] = online['true_slots'].apply(lambda x: list_tuple_2_str(x))
    offline['pile'] = offline['true_slots'].apply(lambda x: list_tuple_2_str(x))
    offline = offline.apply(lambda x: write_off_true_domain(x, find_dict), axis=1)
    online = online.sort_values(by=['corpus_context', 'pile'])
    offline = offline.sort_values(by=['corpus_context', 'pile'])
    # 保存排序过后的两个表
    offline.to_excel('offline_sorted.xlsx', encoding='utf-8')
    online.to_excel('online_sorted.xlsx', encoding='utf-8')
    online = online.reset_index(drop=True)
    offline = offline.reset_index(drop=True)
    offline['corpus_id'] = online['corpus_id']
    offline['domain_intent'] = online['domain_intent']
    for i in range(len(online)):
        merge_data.loc[i] = compare_online_offline(online.loc[i], offline.loc[i])
    merge_data = pre_compare_result(merge_data)
    merge_data.to_excel('merge_data.xlsx', encoding='utf-8')
    return merge_data


def list_tuple_2_str(x):
    x = sorted(x)
    pile = ''
    for i in x:
        pile = pile + ''.join(i)
    return pile


def compare_online_offline(online, offline):
    # 需要online和offline的数据都同时拥有完整true信息，包含domain，intent，slots
    # 若未构建offline的true_slots，则运行下行，否则注释掉
    offline['true_slots'] = online['true_slots']
    if online['corpus_context'] == offline['corpus_context']:
        if online['pred_domain_name'] == online['true_domain_name'] and offline['true_domain_name'] == online['true_domain_name']:
            offline['pred_domain_name'] = online['pred_domain_name']
            if online['pred_intent_name'] == online['true_intent_name'] and online['true_intent_name'] == offline['true_intent_name']:
                offline['pred_intent_name'] = online['pred_intent_name']
                if online['pred_slots'] == online['true_slots'] and offline['true_slots'] == online['true_slots']:
                    offline['pred_slots'] = online['pred_slots']
    offline['corpus_id'] = online['corpus_id']
    offline['domain_intent'] = online['domain_intent']
    return offline



def write_off_true_domain(x, find_dict):
    for k, v in find_dict.items():
        if x['true_intent_name'] == v:
            x['true_domain_name'] = k
        if x['pred_intent_name'] == v:
            x['pred_domain_name'] = k
    return x


def dic_in_list_sorted(list_data):
    mid_result = {}
    for x in list_data:
        for k, v in x.items():
            mid_result[k] = v
    return_result = sorted(mid_result.items(), key=lambda i: i[0])
    return return_result


def pre_compare_result(data):
    data['compare_result'] = data.apply(lambda x: ifequal(x), axis=1)
    # data['compare_result'] = data.apply(ifequal(data), axis=1)
    return data


def ifequal(x):
    if x['pred_domain_name'] != x['true_domain_name']:
        return 1
    elif x['pred_intent_name'] != x['true_intent_name']:
        return 2
    elif x['pred_slots'] != x['true_slots']:
        return 3
    else:
        return 4


def offline_data_2_xlsx(filepath):
    # offline_data = pd.read_table(filepath, sep='\t', header=None)
    offline_data = pd.DataFrame(columns=['corpus_context', 'pred_domain_name', 'pred_intent_name', 'pred_slots', 'true_domain_name', 'true_intent_name', 'true_slots'])
    off_pred_data = codecs.open(filepath, 'r', encoding='utf-8')
    off_pred_data = json.load(off_pred_data)
    for one_pred_data in off_pred_data:
        corpus_context = ''.join(one_pred_data['seq_in'])
        # 如果离线模型预测输出包含domain和intent，并且是用 “ | ”做分割的：
        # pred_domain_name, pred_intent_name = one_pred_data['pred'].split('|')
        # true_domain_name, true_intent_name = one_pred_data['label'].split('|')
        # pred_domain_name = one_pred_data['pred'][1]
        # true_domain_name = one_pred_data['label'][1]
        pred_intent_name = one_pred_data['pred'][0]
        true_intent_name = one_pred_data['label'][0]
        pred_slots, true_slots, true_domain_name, pred_domain_name = [], [], [], []
        offline_data.loc[len(offline_data)] = [corpus_context, pred_domain_name, pred_intent_name, pred_slots, true_domain_name, true_intent_name, true_slots]
    offline_data.to_excel(filepath.replace('.txt', '.xlsx'), encoding='utf-8')
    return offline_data


def main():
    online_data = select_data('bvt_5.csv')
    offline_data = offline_data_2_xlsx('test_merge_all_eval.txt')
    merge_data = merge_pt_out(online_data, offline_data)


if __name__ == '__main__':
    main()