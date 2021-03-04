import random
import codecs
from collections import defaultdict


def Test_2_100_300(path, filename):
    domain_intent_name_txt_100 = codecs.open(path + 'support_100.txt', 'w', encoding='utf-8')
    domain_intent_name_txt_50 = codecs.open(path + 'support_50.txt', 'w', encoding='utf-8')
    domain_intent_name_txt_5 = codecs.open(path + 'support_5.txt', 'w', encoding='utf-8')
    domain_intent_name_txt_300 = codecs.open(path + 'correct_300.txt', 'w', encoding='utf-8')
    data_dict = defaultdict(list)

    with open(path + filename, 'r', encoding='utf-8') as f:
        datas = f.readlines()
        for data in datas:
            context, domain, intent, con_slots = data.split()
            key = domain + '.' + intent
            if key == 'news.search':
                intent = 'search_' + key.split('.')[0]
            elif key == 'geography.capital':
                intent = 'search_' + key.split('.')[1]
            data = context + '\t' + domain + '\t' + intent + '\t' + con_slots + '\n'
            data_dict[key].append(data)

    random.seed(0)
    for k, _ in data_dict.items():
        random.shuffle(data_dict[k])

    for k, v in data_dict.items():
        count = 1
        for data in v:
            if count > 100:
                domain_intent_name_txt_300.write(data)
            else:
                domain_intent_name_txt_100.write(data)
                if count <= 50:
                    domain_intent_name_txt_50.write(data)
                if count <= 5:
                    domain_intent_name_txt_5.write(data)
            count += 1

    domain_intent_name_txt_300.close()
    domain_intent_name_txt_100.close()
    domain_intent_name_txt_50.close()
    domain_intent_name_txt_5.close()


if __name__ == '__main__':
    Test_2_100_300('./our_db_test_data/', 'test_data_2000.txt')