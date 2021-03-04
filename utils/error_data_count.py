# coding:utf-8
import json
import codecs
from collections import Counter


def create_json_file(path, filename):
    """
    parameters:path:
    """
    with codecs.open(path + filename, 'r', encoding='utf-8') as f:
        index = 1
        err_index = {}
        err_index['1'] = []
        err_index['3'] = []
        err_index['6'] = []
        datas = f.readlines()
        counts = []
        for data in datas:
            length = len(data.strip().split('\t'))
            if length == 1:
                err_index['1'].append(index)
            elif length == 3:
                err_index['3'].append(index)
            elif length == 6:
                err_index['6'].append(index)
            index += 1
            counts.append(length)
        di_counts = Counter(counts)
        with codecs.open('dom_int_length.txt', 'w', encoding='utf-8') as d:
            for k, v in di_counts.items():
                d.write(str(k) + '\t' + str(v) + '\n')
        with codecs.open('err_length_data.json', 'w', encoding='utf-8') as t:
            json.dump(err_index, t, indent=2)

    return di_counts


path = "D:\Git\Git项目\MetaDialog\data\\few_slot_learning\\"
filename = "few_slot_learning_result.txt"
jsonfilename = "few_slot_data"

if __name__ == '__main__':
    result = create_json_file(path, filename, jsonfilename)