import codecs
import json
import random
import re

random.seed(0)


def select_data_2_train_or_test(source_data_path, source_data_filename, select_domain_intent_list: list,
                                each_intent_num, old_training_json_file=None, out_put_json_file='select_data_2_train_or_test.json'):
    """
    :param source_data_path:
    :param source_data_filename:
    :param select_domain_intent_list:
    :param each_intent_num: choose sample num
    :param old_training_json_file: old training or testing data file name
    :param out_put_json_file: output json file name
    :return: json file,contais old training or testing data and new select data
    """
    with codecs.open(source_data_path + source_data_filename, 'r', encoding='utf-8') as f:
        all_datas = f.readlines()
        select_data = {}
        for do_in_save_list in select_domain_intent_list:
            select_data[do_in_save_list] = []
        for data in all_datas:
            mid_dic = {}
            if len(data.strip().split('\t')) == 4:
                contexts, domain, intent, contexts_slots = data.strip().split('\t')
                mid_dic['domain'] = domain
                mid_dic['text'] = contexts
                mid_dic['intent'] = intent
                mid_dic['slots'] = {}
                pattern = r'<(.+?)>(.+?)<'
                res = re.findall(pattern, contexts_slots)
                for name in res:
                    mid_dic['slots'][name[0]] = name[1]
                do_in = domain + '|' + intent
                if do_in in select_domain_intent_list:
                    select_data[do_in].append(mid_dic)
        if old_training_json_file:
            with codecs.open(old_training_json_file, 'r+', encoding='utf-8') as t:
                res = json.load(t)
        else:
            res = []
        for k, v in select_data.items():
            if len(v) < each_intent_num:
                raise ValueError("Select data Number = {}, Less than {}".format(len(v), each_intent_num))
            random.shuffle(v)
            select_data[k] = v[:each_intent_num]
            for sample in select_data[k]:
                res.append(sample)
        t = codecs.open(source_data_path + out_put_json_file, 'w', encoding='utf-8')
        json.dump(res, t, ensure_ascii=False, indent=2)
        t.close()


if __name__ == '__main__':
    source_data_path = '../bvt_cal/PRCalculator/'
    source_data_filename = 'select_from_data.txt'
    select_domain_intent_list = ['flash_briefing|search', 'taxi|call', 'globalctrl|turn_down']
    each_intent_num = 200
    old_training_json_file = '../bvt_cal/PRCalculator/source.json'
    select_data_2_train_or_test(source_data_path, source_data_filename, select_domain_intent_list, each_intent_num, old_training_json_file)