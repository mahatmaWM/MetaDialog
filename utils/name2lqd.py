import codecs
import json
import re

rename_domains_100_dict = {
    'almanac': 'huangli_100-1362948838480896000',
    'disease': 'jibing_100-1362963779678068736',
    'geography': 'shoudu_100-1363009765788008448',
    'news': 'xinwen_100-1362971025342423040',
    'weather': 'tianqi_100-1362964723065118720',
    'kefu_quqian': 'kefu_quqian_100-1369110629883752448',
    'kefu_rengong': 'zhegeshiyaoshanchude'
}
rename_domains_50_dict = {
    'almanac': 'huangli_50-1362949324646834176',
    'disease': 'jibing_50-1362964399281672192',
    'geography': 'shoudu_50-1363010714585796608',
    'news': 'xinwen_50-1362971796507201536',
    'weather': 'tianqi_50-1362968915859169280',
    'kefu_quqian': 'kefu_quqian_50-1369111325655871488',
    'kefu_rengong': 'kefu_rengong_50-1369111599451660288'
}
rename_domains_5_dict = {
    'almanac': 'huangli_5-1362949499880652800',
    'disease': 'jibing_5-1362964556333105152',
    'geography': 'shoudu_5-1363011111425675264',
    'news': 'xinwen_5-1363008185919516672',
    'weather': 'tianqi_5-1362970384020725760',
    'kefu_quqian': 'kefu_quqian_5-1369111467322683392',
    'kefu_rengong': 'kefu_rengong_5-1369111738115383296'
}


def Name2lqd(path, filenames, output1, output2, rename_domain_dict, sup_que_for_pingtai=False, support_mode=100):
    """
    :param path: file path
    :param filenames:
    :param output1: output .txt file
    :param output2: output .json file
    :param rename_domain_dict: rename domain name into project name
    :param sup_que_for_pingtai: Whether to split into upload platform form
    :param support_mode: Support set usage
    :return:
    """
    out_data_txt = codecs.open(path + output1, 'w', encoding='utf-8')
    out_data_json = codecs.open(path + output2, 'w', encoding='utf-8')
    dump_file = []
    re_datas = []
    with codecs.open(path + filenames, 'r', encoding='utf-8') as f:
        for data in f.readlines():
            context, domain, intent, con_slots = data.strip().split('\t')
            new_domain = rename_domain_dict[domain]
            result = {}
            result['text'] = context
            result['domain'] = 'test_support_mode_' + str(support_mode)
            result['intent'] = new_domain + '.' + intent
            result['slots'] = {}
            pattern = r'<(.+?)>(.+?)<'
            res = re.findall(pattern, con_slots)
            for name in res:
                result['slots'][name[0]] = name[1]
            dump_file.append(result)

            re_data = context + '\t' + new_domain + '\t' + intent + '\t' + con_slots + '\n'
            re_datas.append(re_data)
        json.dump(dump_file, out_data_json, ensure_ascii=False, indent=2)
    for re_data in re_datas:
        out_data_txt.write(re_data)
    out_data_txt.close()
    out_data_json.close()

    if sup_que_for_pingtai:
        for k, v in rename_domain_dict.items():
            with codecs.open(path + 'support_pingtai/' + v + '_support_2_pingtai.txt', 'w', encoding='utf-8') as open_file_1:
                for re_data in re_datas:
                    context, domain, intent, con_slots = re_data.strip().split('\t')
                    if domain == v:
                        open_file_1.write(con_slots + '\n')
        if output1.split('_')[0] == 'correct':
            with codecs.open(path + 'support_pingtai/' + output1.replace('.txt', '_test_set.txt'), 'w', encoding='utf-8') as open_file_2:
                for re_data in re_datas:
                    context, domain, intent, con_slots = re_data.strip().split('\t')
                    test_set = domain + '|' + intent + '|||' + con_slots + '\n'
                    open_file_2.write(test_set)


if __name__ == '__main__':
    Name2lqd('./our_db_test_data/',
             filenames='correct_300.txt',
             output1='correct_100_for_pingtai.txt',
             output2='correct_100.json',
             rename_domain_dict=rename_domains_100_dict,
             support_mode=100)
    Name2lqd('./our_db_test_data/',
             filenames='correct_300.txt',
             output1='correct_50_for_pingtai.txt',
             output2='correct_50.json',
             rename_domain_dict=rename_domains_50_dict,
             support_mode=50)
    Name2lqd('./our_db_test_data/',
             filenames='correct_300.txt',
             output1='correct_5_for_pingtai.txt',
             output2='correct_5.json',
             rename_domain_dict=rename_domains_5_dict,
             support_mode=5)
    Name2lqd('./our_db_test_data/',
             filenames='correct_300.txt',
             output1='correct_2_for_pingtai.txt',
             output2='correct_2.json',
             rename_domain_dict=rename_domains_5_dict,
             support_mode=2)

    Name2lqd('./our_db_test_data/',
             filenames='support_100.txt',
             output1='support_100_for_pingtai.txt',
             output2='support_100.json',
             rename_domain_dict=rename_domains_100_dict,
             support_mode=100)
    Name2lqd('./our_db_test_data/',
             filenames='support_50.txt',
             output1='support_50_for_pingtai.txt',
             output2='support_50.json',
             rename_domain_dict=rename_domains_50_dict,
             support_mode=50)
    Name2lqd('./our_db_test_data/',
             filenames='support_5.txt',
             output1='support_5_for_pingtai.txt',
             output2='support_5.json',
             rename_domain_dict=rename_domains_5_dict,
             support_mode=5)
    Name2lqd('./our_db_test_data/',
             filenames='support_2.txt',
             output1='support_2_for_pingtai.txt',
             output2='support_2.json',
             rename_domain_dict=rename_domains_5_dict,
             support_mode=2)


