#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 18-12-26 下午4:36
# @Email : jacobjzhang@tencent.com
# @File  : compare_based.py

"""对比错误等级"""

import copy
import pandas as pd


class CompareBased(object):
    def __init__(self,
                 # compare_columns_pairs,  # 对比列
                 # data_frame
                 ):
        # self.compare_columns_pairs = compare_columns_pairs
        # self.data_frame = data_frame
        self.compare_columns_pairs = None
        self.data_frame = None
        pass

    def compare_unit(self, data_dict):
        """计算每一行的错误等级"""
        compare_pairs = []
        for compare_column_pair in self.compare_columns_pairs:
            com_pair1 = data_dict[compare_column_pair[0]]
            com_pair2 = data_dict[compare_column_pair[1]]
            compare_pairs.append([com_pair1, com_pair2])

        error_level = 0
        for pairs in compare_pairs:
            error_level += 1
            if pairs[0] != pairs[1]:
                return error_level
        return error_level + 1

    def compare(self, data_frame, compare_columns, result_column=None):
        if not result_column:
            result_column = 'compare_result'

        self.compare_columns_pairs = []
        for columns in compare_columns:
            self.compare_columns_pairs.append(
                ['true_' + columns, 'pred_' + columns]
            )

        self.data_frame = data_frame

        data_list = list(self.data_frame.to_dict(orient='index').values())

        for data_dict in data_list:
            data_dict[result_column] = self.compare_unit(data_dict)

        self.data_frame = pd.DataFrame(data_list)
        return self.data_frame

    @staticmethod
    def sub_list(list1, list2):
        """判断A是否为B的子集"""
        list1 = copy.deepcopy(list1)
        list2 = copy.deepcopy(list2)

        for element in list1:
            if element in list2:
                list2.remove(element)
            else:
                return False
        return True


class ModuleCompare(CompareBased):
    def __init__(self):
        super(ModuleCompare, self).__init__()

    def sort_struct(self, struct):
        """支持dict, list嵌套排序"""
        if isinstance(struct, list):
            if struct and len(struct) == 0:
                return
            elif isinstance(struct[0], str):
                struct.sort()

            elif isinstance(struct[0], dict):
                for tmp_struct in struct:
                    for key in tmp_struct:
                        self.sort_struct(tmp_struct[key])
        elif isinstance(struct, dict):
            for key in struct:
                self.sort_struct(struct[key])

    def compare_ner(self, ner_true, ner_pred):
        final_flag = True
        for ner_dict in ner_true:
            for key, values in ner_dict.iteritems():
                key_flag = False
                for value in values:
                    tmp_dict = {value: [key]}
                    flag = self.compare_ner_unit(ner_true=tmp_dict, ner_pred=ner_pred)
                    key_flag |= flag
                    if key_flag:
                        break
                final_flag &= key_flag
                if not final_flag:
                    break
        return final_flag

    def compare_ner_unit(self, ner_true, ner_pred):
        """ner的结果判断标准为： ner_true是ner_pred的子集
            ner_pred = {"sys.music.singer": ["张学友", "刘德华", "刘德华"],
                "sys.music.song": ["忘情水"]
                }

            ner_true = {"sys.music.singer": ["刘德华", "张学友"]
                }

            >> True

        """
        if not self.sub_list(ner_true.keys(), ner_pred.keys()):
            return False
        else:
            for key, true_value in ner_true.iteritems():
                if not self.sub_list(true_value, ner_pred[key]):
                    return False
        return True

    def compare_dclf(self, dclf_true, dclf_pred):
        """dclf判断标准, dclf_true是dclf_pred的子集
            dclf_pred = ["music", "video", "fm"]
            dclf_true = ['music']
            >> True
        """
        # print dclf_true
        # print dclf_pred
        # print '---'
        return self.sub_list(dclf_true, dclf_pred)

    def compare_iclf(self, iclf_true, iclf_pred):
        """iclf判断标准, iclf_true是iclf_pred的子集
            iclf_pred = ["music.play", "music.favor", "fm.play"]
            iclf_true = ['music.play']
            >> True
        """
        return self.sub_list(iclf_true, iclf_pred)

    def compare_se(self, se_true, se_pred):
        """se判断标准, se_true是se_pred的子集
            se_pred = [
                {"music.singer": ["刘德华", "刘德华", "张雪友"],
                 "music.song": ["忘情水"]
                 },
                {"fm.anchor": ["刘德华", "刘德华", "张雪友"],
                 "fm.album": ["忘情水"]
                 },
                {"music.singer": ["刘德华", "刘德华和张雪友"],
                 "music.song": ["忘情水"]
                 }
            ]

            se_true = [{"music.singer": ["刘德华",  "张雪友", "刘德华"],
                       "music.song": ["忘情水"]
                       }]
            >> True
        """
        # print 'se_true'
        # print se_true
        # print se_pred
        # print 'se end'
        self.sort_struct(se_true)
        self.sort_struct(se_pred)
        # for tmp_se in se_true:
        #     for key, value in tmp_se.iteritems():
        #         value.sort()
        # for tmp_se in se_pred:
        #     for key, value in tmp_se.iteritems():
        #         value.sort()

        return self.sub_list(se_true, se_pred)

    def __compare_corpus(self, corpus_true, corpus_pred):
        """
        corpus_true结果是corpus_pred的子集
        corpus_pred = [
            {"domain": "music",
             "intent": "play",
             "slots": {"music.singer": ["刘德华", "张学友", "刘德华"],
                       "music.song": ["忘情水"]
                       }
             },
            {"domain": "fm",
             "intent": "play",
             "slots": {"fm.anchor": ["刘德华", "张学友", "刘德华"],
                       "fm.album": ["忘情水"]
                       }
             },
            {"domain": "music",
             "intent": "play",
             "slots": {"music.singer": ["刘德华", "刘德华和张学友"],
                       "music.song": ["忘情水"]
                       }
             },
        ]
        corpus_true = [
            {"domain": "music",
             "intent": "play",
             "slots": {"music.singer": ["刘德华",   "张学友", "刘德华"],
                       "music.song": ["忘情水"]
                       }
             }
        ]
        >> True
        """
        self.sort_struct(corpus_true)
        self.sort_struct(corpus_pred)
        return self.sub_list(corpus_true, corpus_pred)

    def compare_corpus_reg(self, corpus_true, corpus_pred):
        return self.__compare_corpus(corpus_true, corpus_pred)

    def compare_corpus_model(self, corpus_true, corpus_pred):
        return self.__compare_corpus(corpus_true, corpus_pred)

    def compare_pattern(self, pattern_true, pattern_pred):
        return self.__compare_corpus(corpus_true=pattern_true, corpus_pred=pattern_pred)

    def compare_dm_ranking(self, dm_true, dm_pred):
        return self.__compare_corpus(corpus_true=dm_true, corpus_pred=dm_pred)


if __name__ == "__main__":
    NER_PRED = {
        'sys.music.singer': [u'刘德华'],
        'sys.music.hot_singer': [u'刘德华'],
        'sys.music.hot_song': [u'冰雨'],
        'sys.music.song': [u'冰雨']
    }

    NER_TRUE = [
        {u'刘德华': ['sys.music.singer', 'sys.music.hot_singer']},
        {u'冰雨': ['sys.music.hot_song', 'sys.music.song']
         }
    ]

    compare_handle = ModuleCompare()
    print(compare_handle.compare_ner(ner_pred=NER_PRED, ner_true=NER_TRUE))
