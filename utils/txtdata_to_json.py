# coding:utf-8
import json
import os
import re


def create_json_file(path, filename, jsonfilename):
    """
    parameters:path:
    """
    with open(path + filename, 'r', encoding='utf-8') as f:
        datas = f.readlines()
        dump_file = []
        with open(path + jsonfilename + '.json', 'a', encoding='utf-8') as t:
            for data in datas:
                result = {}
                text, domain, intent, label_context = data.strip().split('\t')
                result['text'] = text
                result['domain'] = domain
                result['intent'] = intent
                result['slots'] = {}
                pattern = r'<(.+?)>(.+?)<'
                res = re.findall(pattern, label_context)
                for name in res:
                    result['slots'][name[0]] = name[1]
                dump_file.append(result)
            json.dump(dump_file, t, ensure_ascii=False, indent=2)
    return result


if __name__ == '__main__':
    path = 'F:\git\MetaDialog\data\\few_slot_learning\data_out\\300test_2_100_50_5\\'
    filename = '50_support.txt'
    jsonfilename = 'dev_support'
    res = create_json_file(path, filename, jsonfilename)