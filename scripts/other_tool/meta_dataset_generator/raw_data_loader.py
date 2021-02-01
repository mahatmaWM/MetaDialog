# coding: utf-8
# author: Atma Hou
from typing import Dict, List, Tuple
import os
import re
import json


class RawDataLoaderBase:
    """ Load raw data"""
    def __init__(self, opt):
        self.opt = opt

    def load_data(self, path: str) -> dict:
        """
        Load all data into one dict.
        :param path: path to the file or dir of data
        :return: a dict store all data: {"partition/domain name" : { 'seq_ins':[], 'labels'[]:, 'seq_outs':[]}}
        """
        raise NotImplementedError




class SMPDataLoader(RawDataLoaderBase):
    """ data loader for SMP (Chinese) data """

    def __init__(self, opt):
        super(SMPDataLoader, self).__init__(opt)

    def load_data(self, path: str, with_dev: bool = True):
        """
        Load all data into one dict.
        :param path: path to the file or dir of data
        :param with_dev: decide whether handle dev data or not
        :return:
            a dict store train data:  {"partition/domain name" : { 'seq_ins':[], 'labels'[]:, 'seq_outs':[]}}
            +
            a dict store dev & test data: {"partition/domain name" : { 'seq_ins':[], 'labels'[]:, 'seq_outs':[]}}
            +
            a dict store support data: {"partition/domain name" : { 'seq_ins':[], 'labels'[]:, 'seq_outs':[]}}
        """
        print('Start loading SMP (Chinese) data from: ', path)
        all_data = {}

        all_files = [os.path.join(path, 'train', filename)
                     for filename in os.listdir(os.path.join(path, 'train')) if filename.endswith('.json')]

        for one_file in all_files:
            part_data = self.unpack_train_data(one_file)

            for domain, data in part_data.items():
                if domain not in all_data:
                    all_data[domain] = {"seq_ins": [], "seq_outs": [], "labels": []}
                all_data[domain]['seq_ins'].extend(part_data[domain]['seq_ins'])
                all_data[domain]['seq_outs'].extend(part_data[domain]['seq_outs'])
                all_data[domain]['labels'].extend(part_data[domain]['labels'])

        dev_data, support_data = {}, {}
        if with_dev:
            dev_support_files = [os.path.join(path, 'dev/support', filename)
                                 for filename in os.listdir(os.path.join(path, 'dev/support'))
                                 if filename.endswith('.json')]
            support_data, support_text_set = self.unpack_support_data(dev_support_files)

            dev_all_files = [os.path.join(path, 'dev/correct', filename)
                             for filename in os.listdir(os.path.join(path, 'dev/correct'))
                             if filename.endswith('.json')]
            for one_file in dev_all_files:
                part_data = self.unpack_train_data(one_file, support_text_set)

                for domain, data in part_data.items():
                    if domain not in all_data:
                        dev_data[domain] = {"seq_ins": [], "seq_outs": [], "labels": []}
                    dev_data[domain]['seq_ins'].extend(part_data[domain]['seq_ins'])
                    dev_data[domain]['seq_outs'].extend(part_data[domain]['seq_outs'])
                    dev_data[domain]['labels'].extend(part_data[domain]['labels'])

        return {'train': all_data, 'dev': dev_data, 'support': support_data}

    def unpack_support_data(self, all_data_path):
        support_data = {}
        support_text_set = set()
        for data_path in all_data_path:

            with open(data_path, 'r', encoding='utf-8') as reader:
                json_data = json.load(reader)

            print('support data num: {} - {}'.format(len(json_data), data_path))

            for item in json_data:
                domain = item['domain']
                support_text_set.add(item['text'])

                if domain not in support_data:
                    support_data[domain] = {"seq_ins": [], "seq_outs": [], "labels": []}

                seq_in, seq_out, label = self.handle_one_utterance(item)

                support_data[domain]['seq_ins'].append(seq_in)
                support_data[domain]['seq_outs'].append(seq_out)
                support_data[domain]['labels'].append([label])

        return support_data, support_text_set

    def unpack_train_data(self, data_path: str, remove_set: set = None):
        part_data = {}
        with open(data_path, 'r', encoding='utf-8') as reader:
            json_data = json.load(reader)

        print('all data num: {} - {}'.format(len(json_data), data_path))

        for item in json_data:
            domain = item['domain']
            if domain not in part_data:
                part_data[domain] = {"seq_ins": [], "seq_outs": [], "labels": []}

            seq_in, seq_out, label = self.handle_one_utterance(item)
            part_data[domain]['seq_ins'].append(seq_in)
            part_data[domain]['seq_outs'].append(seq_out)
            part_data[domain]['labels'].append([label])

        return part_data

    def handle_one_utterance(self, item):
        text = item['text'].replace(' ', '')
        seq_in = list(text)

        slots = item['slots']
        seq_out = ['O'] * len(seq_in)
        for slot_key, slot_value in slots.items():
            if not isinstance(slot_value, list):
                slot_value = [slot_value]
            for s_val in slot_value:
                s_val = s_val.replace(' ', '')
                if s_val in text:
                    s_idx = text.index(s_val)
                    s_end = s_idx + len(s_val)
                    seq_out[s_idx] = 'B-' + slot_key
                    for idx in range(s_idx + 1, s_end):
                        seq_out[idx] = 'I-' + slot_key
                else:
                    print('text: {}'.format(text))
                    print('  slot_key: {} - slot_value: {}'.format(slot_key, s_val))

        label = item['intent']

        return seq_in, seq_out, label


if __name__ == '__main__':
    print('Start unit test.')
    import argparse
    parse = argparse.ArgumentParser()
    opt = parse.parse_args()
    opt.intent_as_domain = False
    opt.task = 'sc'
    opt.dataset = 'smp'
    opt.label_type = 'intent'

    smp_path = '/Users/lyk/Work/Dialogue/FewShot/SMP/'
    smp_loader = SMPDataLoader(opt)

    smp_data = smp_loader.load_data(path=smp_path)
    train_data, dev_data, support_data = smp_data['train'], smp_data['dev'], smp_data['support']

    print("train: smp domain number: {}".format(len(train_data)))
    print("train: all smp domain: {}".format(train_data.keys()))
    print("dev: smp domain number: {}".format(len(dev_data)))
    print("dev: all smp domain: {}".format(dev_data.keys()))
    print("support: smp domain number: {}".format(len(support_data)))
    print("support: all smp domain: {}".format(support_data.keys()))

    print("support: {}".format(support_data))


