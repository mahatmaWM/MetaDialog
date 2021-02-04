import os
import json

def creat_ds_set(data_path: str, remove_set: set = None):
    domain = set()
    slots = set()
    with open(data_path, 'r', encoding='utf-8') as reader:
        json_data = json.load(reader)

    for item in json_data:
        domain.add(item['domain'] + '|' + item['intent'])
        for key, items in item['slots'].items():
            slots.add(key)

    return domain, slots

def domain_file_count(path, file_dicname):
    dic = {}
    dic[file_dicname + '_domain'] = set()
    dic[file_dicname + '_slots'] = set()
    all_train_files = [os.path.join(path, file_dicname, filename) for filename in
                       os.listdir(os.path.join(path, file_dicname)) if filename.endswith('.json')]

    for file in all_train_files:
        domain, slots = creat_ds_set(file)
        dic[file_dicname + '_domain'] = domain | dic[file_dicname + '_domain']
        dic[file_dicname + '_slots'] = slots | dic[file_dicname + '_slots']

    return dic[file_dicname + '_domain'], dic[file_dicname + '_slots']


def load_data(path: str, with_dev: bool = True):
    """
    to count all domain and slots, which use to train and test
    """
    print('Start loading data from: ', path)
    all_count = {}
    train_count = {}
    dev_count = {}
    test_count = {}
    train_domain, train_slots = domain_file_count(path, 'train')
    dev_support_domain, dev_support_slots = domain_file_count(path, 'dev/support')
    dev_correct_domain, dev_correct_slots = domain_file_count(path, 'dev/correct')
    test_support_domain, test_support_slots = domain_file_count(path, 'test/support')
    test_correct_domain, test_correct_slots = domain_file_count(path, 'test/correct')
    train_count['train_domain'] = train_domain
    train_count['train_slots'] = train_slots
    dev_count['dev_support_domain'] = dev_support_domain
    dev_count['dev_support_slots'] = dev_support_slots
    dev_count['dev_correct_domain'] = dev_correct_domain
    dev_count['dev_correct_slots'] = dev_correct_slots
    test_count['test_support_domain'] = test_support_domain
    test_count['test_support_slots'] = test_support_slots
    test_count['test_correct_domain'] = test_correct_domain
    test_count['test_correct_slots'] = test_correct_slots
    all_count['train_count'] = train_count
    all_count['dev_count'] = dev_count
    all_count['test_count'] = test_count
    with open(path + '_describe.txt', 'a', encoding='utf-8') as f:
        for key,item in all_count.items():
            for k, v in item.items():
                f.write(k+'\t'+str(len(v))+'\n')
                f.write(str(v) + '\n')
    return all_count



if __name__ == '__main__':
    create = load_data('D:\Git\Git项目\MetaDialog\FewJoint\SMP_Final_Origin2_3')
    print(create)