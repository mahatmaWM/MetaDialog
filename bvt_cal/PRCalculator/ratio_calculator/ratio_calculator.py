"""
# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
-----------------------------------------------------------------------------
    File Name:     ratio_calculator
    Author:        jacobjzhang
    Date:          2020/6/29 20:38
-----------------------------------------------------------------------------
    Description: NotImplemented
"""

import pandas as pd


class RatioCalculator(object):
    def __init__(self,
                 unique_columns,  # 表示在统计前去重的条件
                 data_frame,
                 agg_columns,  # 按哪些列进行聚合
                 ):
        self.unique_columns = list(unique_columns)
        self.agg_columns = list(agg_columns)
        self.data_frame = data_frame

    def cal(self):
        metrics_df = self.data_frame.groupby(by=self.agg_columns).size().reset_index(name='count')
        metrics_df['all_num'] = len(self.data_frame.drop_duplicates(self.unique_columns))
        metrics_df['ratio'] = metrics_df['count'] *1.0/metrics_df['all_num']

        return metrics_df, self.data_frame


if __name__ == "__main__":
    df = pd.read_excel('0601_0615final_case.xlsx')[['错误原因', 'log_id', 'ds']]

    data_list = df.to_dict(orient='index').values()
    for data_dict in data_list:
        if data_dict['错误原因'] in ['槽位提取错误', '意图分类错误', '领域分类错误']:
            data_dict['ratio_type'] = '语义错误'
        else:
            data_dict['ratio_type'] = data_dict['错误原因']

    df = pd.DataFrame(data_list)
    agg_columns = ('ratio_type', '错误原因',)
    unique_columns = ('log_id',)
    ratio_calculator = RatioCalculator(agg_columns=agg_columns,
                                       unique_columns=unique_columns,
                                       data_frame=df)
    statistics_df1, data_frame = ratio_calculator.cal()
    print(statistics_df1)
