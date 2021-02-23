#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 18-12-21 下午8:47
# @Email : jacobjzhang@tencent.com
# @File  : online_data_format.py

import pandas as pd
import re
import json


def format_dm_di_unit(dm_di):
    domain_name = dm_di['domain_name']
    intent_name = dm_di['intent_name']
    slots_map_text = dm_di['slotsMap']
    params = []
    for tmp_map in slots_map_text:
        for key in tmp_map:
            if key == '_offset':
                continue
            else:
                params.append({key: tmp_map[key]})
    params.sort()
    return domain_name, intent_name, json.dumps(params, ensure_ascii=False)


def format_tag_di_unit(tag_di):
    domain_name = tag_di['domain_name']
    intent_name = tag_di['intent_name']
    data = tag_di['data']
    params = []
    reg = re.compile("<(.*?)>(.*?)<")

    results = reg.findall(data)
    for result in results:
        params.append({result[0]: result[1]})

    params.sort()
    return domain_name, intent_name, json.dumps(params, ensure_ascii=False)


def format_unit(corpus_id, session_id, corpus_content, dm_multi_di, tag_multi_di,
                app_key,sampling_type
                # datetime, scene
                ):
    dm_multi_di = json.loads(dm_multi_di, encoding='utf-8')
    tag_multi_di = json.loads(tag_multi_di, encoding='utf-8')
    try:
        corpus_content = corpus_content.decode('utf-8')
    except:
        corpus_content = corpus_content
    # 转换数据
    dm_multi_di_list = []
    for dm_di in dm_multi_di:
        # if 'isMainSemantic' in dm_di and dm_di['isMainSemantic'] == True:
            dm_multi_di_list.append(format_dm_di_unit(dm_di))

    if len(dm_multi_di_list) == 0:
        dm_multi_di_list.append(['', '', json.dumps([])])

    tag_multi_di_list = []
    for tag_di in tag_multi_di:
        tag_multi_di_list.append(format_tag_di_unit(tag_di))

    # 组装每一行数据
    return_list = []
    for dm_di in dm_multi_di_list:
        sys_domain, sys_intent, sys_slots = dm_di
        for tag_di in tag_multi_di_list:
            human_domain, human_intent, human_slots = tag_di

            return_list.append([corpus_id, session_id, corpus_content,
                                sys_domain, sys_intent, sys_slots,
                                human_domain, human_intent, human_slots,
                                app_key,sampling_type
                                # datetime, scene
                                ])
    return return_list


def format(datas):
    format_list = []
    for data in datas:
        corpus_id, session_id, corpus_content, dm_multi_di, tag_multi_di, app_key, sampling_type = data
        # corpus_id, session_id, corpus_content, dm_multi_di, tag_multi_di, datetime, scene = data
        try:
            format_list += format_unit(corpus_id, session_id, corpus_content, dm_multi_di, tag_multi_di,
                                       app_key,sampling_type
                                       # datetime, scene
                                       )
        except Exception:
            continue
    df = pd.DataFrame(format_list, columns=['corpus_id', 'session_id', 'corpus_content',
                                            'pred_domain_name', 'pred_intent_name', 'pred_slots',
                                            'true_domain_name', 'true_intent_name', 'true_slots',
                                            'app_key', 'sampling_type'
                                            # 'datetime', 'current_scene'
                                            ])
    return df