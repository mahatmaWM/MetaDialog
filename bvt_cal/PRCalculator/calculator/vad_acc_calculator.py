#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 * Tencent is pleased to support the open source community by making Angel available.
 *
 * Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
 *
 * Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 *
 * https://opensource.org/licenses/BSD-3-Clause
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is
 * distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific language governing permissions and
 * limitations under the License.
-------------------------------------------------
   Project Name:   OnlineQualityEvaluate
   File Name：     vad_acc_calculator
   Description :
   Author :       jacobjzhang
   date：          2020/3/20 下午1:22
-------------------------------------------------
   Change Activity:
                   2020/3/20 下午1:22
-------------------------------------------------
"""


import sys
import pandas as pd

# reload(sys)
sys.setdefaultencoding('utf-8')


class VadCalculator(object):
    def __init__(self,
                 data_frame,
                 agg_columns,
                 unique_columns,
                 filter_level=0,
                 right_level_column='cut_correct',
                 statistics_level=1
                 ):
        self.data_frame = data_frame
        self.unique_columns = unique_columns
        self.agg_columns = list(agg_columns)
        self.filter_level = filter_level
        self.right_level_column = right_level_column
        self.statistics_level = statistics_level

        self.vad_unique_columns = list(set(self.unique_columns + self.agg_columns))

    def _case_type(self, data_frame):
        data_list = data_frame.to_dict(orient='index').values()
        for i, data_dict in enumerate(data_list):

            if data_dict['is_right'] == 1:
                data_dict['case_type'] = 'VadRight'
            elif data_dict['is_right'] == 0:
                data_dict['case_type'] = 'VadWrong'
        self.case_info = pd.DataFrame(data_list)
        return self.case_info

    def drop_by_unique(self, dataframe):
        """每一个unique只保留最大值"""
        # 默认每一个cal_key, 只保留最大compare_result中的一个
        dataframe = dataframe.drop_duplicates(subset=self.vad_unique_columns)
        return dataframe

    def __trans_statistics_type(self, data_frame):
        data_list = data_frame.to_dict(orient='index').values()
        for i, data_dict in enumerate(data_list):
            if data_dict[self.right_level_column] >= self.statistics_level:
                data_list[i]['is_right'] = 1
                data_list[i]['is_wrong'] = 0
            else:
                data_list[i]['is_right'] = 0
                data_list[i]['is_wrong'] = 1

        data_frame = pd.DataFrame(data_list)
        return data_frame

    def __filter_data(self, data_frame):
        # self.filter_level = filter_level
        dataframe = data_frame[data_frame[self.right_level_column] >= self.filter_level]
        return dataframe

    def cal(self):
        dataframe = self.__filter_data(self.data_frame)
        dataframe = self.drop_by_unique(dataframe=dataframe)
        dataframe = self.__trans_statistics_type(data_frame=dataframe)
        statistics_df1 = dataframe.groupby(by=self.agg_columns)['is_right'].sum().reset_index()
        statistics_df2 = dataframe.groupby(by=self.agg_columns)['is_wrong'].sum().reset_index()

        statistics_df = pd.merge(statistics_df1, statistics_df2, on=self.agg_columns)
        statistics_df[['is_right', 'is_wrong']] = statistics_df[['is_right', 'is_wrong']].astype(int)
        statistics_df = statistics_df.rename(columns={"is_right": "right_num", "is_wrong": "wrong_num"})
        statistics_df = statistics_df.drop_duplicates(subset=self.agg_columns)
        statistics_df['vad_acc'] = statistics_df['right_num'] * 1.0 / (
                statistics_df['right_num'] + statistics_df['wrong_num'])
        case_info = self._case_type(dataframe)

        statistics_df = statistics_df.rename(columns={
            "right_num": "VadRight",
            "wrong_num": "VadWrong"

        })
        return statistics_df, case_info


if __name__ == "__main__":
    df = pd.read_excel(u'已完成_新2019-12-22-925全双工-线上评测.xlsx')
    df['session_id'] = df['sessionID']

    df = df[df['cut_correct'].isin([u'正确', u'错误'])]
    data_list = df.to_dict(orient='index').values()
    for i, data_dict in enumerate(data_list):
        if data_dict['cut_correct'] in [u'正确', '1', 1]:
            data_dict['cut_correct'] = 1
        elif data_dict['cut_correct'] in [u'错误', '0', 0]:
            data_dict['cut_correct'] = 0
        else:
            data_dict['cut_correct'] = -1

    df = pd.DataFrame(data_list)

    vad_handle = VadCalculator(data_frame=df, agg_columns=['domain', ],
                               unique_columns=['session_id', ])
    metrics_df, case_info = vad_handle.cal()
    print(metrics_df)
    print(case_info.head())
