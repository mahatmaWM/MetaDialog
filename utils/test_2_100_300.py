import random
import codecs


def Test_2_100_300(path, filename, domain_intent_name):
    domain_intent_name_txt_100 = codecs.open(path+domain_intent_name + '_100.txt', 'w', encoding='utf-8')
    domain_intent_name_txt_300 = codecs.open(path+domain_intent_name + '_300,txt', 'w', encoding='utf-8')
    data_list = []
    with open(path + filename, 'r', encoding='utf-8') as f:
        datas = f.readlines()
        for data in datas:
            context, domain, intent, con_slots = data.split()
            if domain + '-' + intent == domain_intent_name:
                if domain_intent_name == 'news-search':
                    intent = 'search_' + domain_intent_name.split('-')[0]
                elif domain_intent_name == 'geography-capital':
                    intent = 'search_' + domain_intent_name.split('-')[1]
                data = context + '\t' + domain + '\t' + intent + '\t' + con_slots + '\n'
                data_list.append(data)
        random.shuffle(data_list)
        count = 1
        for data in data_list:
            if count > 100:
                domain_intent_name_txt_300.write(data)
            else:
                domain_intent_name_txt_100.write(data)
            count += 1


if __name__ == '__main__':
    Test_2_100_300('D:\Git\Git项目\MetaDialog\data\\few_slot_learning\data_out\\', 'test_data_2000.txt', 'news-search')