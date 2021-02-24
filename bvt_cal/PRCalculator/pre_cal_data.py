#!/usr/bin/python
# -*- coding:utf-8 -*-

import hashlib
import pandas as pd
import re


def select_data(filename):
    data = pd.read_csv(filename)
    data['true_slots'] = data['人工标注'].apply(lambda x: context2slots(x))
    data['pred_slots'] = data['平台标注'].apply(lambda x: context2slots(x))
    data['corpus_id'] = data['语料'].apply(lambda x: hashlib.md5(x.encode(encoding='UTF-8')).hexdigest())
    res = data[['corpus_id', '语料', '平台领域', '平台意图', 'pred_slots', '人工领域', '人工意图', 'true_slots']].copy()
    # res = merge_pt_out(online=res, outside=None)
    res = res.rename(columns={'语料': 'corpus_content', '平台领域': 'pred_domain_name', '平台意图': 'pred_intent_name', '人工领域': 'true_domain_name', '人工意图': 'true_intent_name'})
    res['domain_intent'] = res['true_domain_name'] + '|' + res['true_intent_name']
    res = pre_compare_result(res)
    res.to_excel('select_data100.xlsx')


def context2slots(contents):
    pattern = r'<(.+?)>(.+?)<'
    result = []
    res = re.findall(pattern, contents)
    if res:
        for name in res:
            res_dic = dict()
            res_dic[name[0]] = name[1]
            result.append(res_dic)
        result = dic_in_list_sorted(result)
    return result


def merge_pt_out(online=None, outside=None):
    pass


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
    # print(x.head())
    if x['pred_domain_name'] != x['true_domain_name']:
        return 1
    elif x['pred_intent_name'] != x['true_intent_name']:
        return 2
    elif x['pred_slots'] != x['true_slots']:
        return 3
    else:
        return 4


if __name__ == '__main__':
    select_data('test100.csv')