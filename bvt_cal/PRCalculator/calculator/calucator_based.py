#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 18-12-26 下午4:52
# @Email : jacobjzhang@tencent.com
# @File  : calucator_based.py

import pandas as pd


class CalculatorBased(object):
    """
    1. 计算每个unique_columns最大的正确等级
    2. 统计每个statistics_columns的正确/错误个数
    """

    def __init__(self,
                 statistics_columns,  # 表示按什么列进行统计结果
                 unique_columns,  # 表示在统计前去重的条件
                 right_level_columns,  # 正确等级的列
                 cut_right_level,  # 表示判断正确的截断等级
                 data_frame,
                 filter_level=None,  # 统计时，需要过滤的等级
                 ):
        self.statistics_columns = list(statistics_columns)
        self.unique_columns = list(unique_columns)
        self.right_level_columns = right_level_columns
        self.cut_right_level = cut_right_level
        self.data_frame = data_frame
        self.filter_level = cut_right_level if filter_level is None else filter_level

        self.data_frame = self.error_level_filter(self.data_frame)

    def error_level_filter(self, dataframe):
        """对错误小于当前统计lever的进行丢弃"""
        dataframe = dataframe[dataframe[self.right_level_columns] >= self.filter_level]
        return dataframe

    def drop_by_unique(self, dataframe):
        """每一个unique只保留最大值"""
        # 默认每一个cal_key, 只保留最大compare_result中的一个
        dataframe = dataframe.sort_values(by=[self.right_level_columns], ascending=False)
        dataframe = dataframe.drop_duplicates(subset=self.unique_columns)
        return dataframe

    def statistics_unit(self, group_df):
        """对每一个统计条件, 计算其中正确的数量和错误的数量"""
        right_num = group_df["is_right"].sum()
        wrong_num = len(group_df) - right_num

        group_df['right_num'] = right_num
        group_df['wrong_num'] = wrong_num
        return group_df

    def statistics(self, data_frame):
        """对每一个统计条件, 计算正确数量和错误数量"""
        # data_frame['is_right'] = data_frame[self.right_level_columns] > self.cut_right_level
        # statistics_df = data_frame.groupby(by=self.statistics_columns).apply(self.statistics_unit)
        # statistics_df = statistics_df.reset_index(drop=True)
        data_frame['is_right'] = (data_frame[self.right_level_columns] > self.cut_right_level).astype('float')
        data_frame['is_wrong'] = (data_frame[self.right_level_columns] <= self.cut_right_level).astype('float')

        # print 'judge is_right time is ', time.time() - start_time
        # statistics_df = data_frame.groupby(by=self.statistics_columns).apply(self.statistics_unit)
        statistics_df1 = data_frame.groupby(by=self.statistics_columns)['is_right'].sum().reset_index()
        statistics_df2 = data_frame.groupby(by=self.statistics_columns)['is_wrong'].sum().reset_index()
        statistics_df = pd.merge(statistics_df1, statistics_df2, on=self.statistics_columns)
        statistics_df[['is_right', 'is_wrong']] = statistics_df[['is_right', 'is_wrong']].astype(int)
        statistics_df = statistics_df.rename(columns={"is_right": "right_num", "is_wrong": "wrong_num"})
        statistics_df = statistics_df.drop_duplicates(subset=self.statistics_columns)
        statistics_columns = self.statistics_columns + ['right_num', 'wrong_num']

        return statistics_df[statistics_columns]

    def cal(self):
        # 按照unique条件进行丢弃动作, 每一个unique条件保留正确等级最大的一个。
        data_frame = self.drop_by_unique(self.data_frame)

        # 按照统计条件,进行统计
        statistics_df = self.statistics(data_frame)
        statistics_df['right_num'] = statistics_df['right_num'].fillna(0.0)
        statistics_df['wrong_num'] = statistics_df['wrong_num'].fillna(0.0)
        return statistics_df

    def cal_case(self):
        """统计case, 同一个unique条件下， 只保留right_level最大的那些列"""
        case_df = self.drop_by_unique(self.data_frame)

        case_df = case_df[self.unique_columns + [self.right_level_columns]]
        case_df = pd.merge(self.data_frame, case_df, on=self.unique_columns + [self.right_level_columns])

        # max_lever = self.data_frame[self.right_level_columns].max()
        # case_df = pd.DataFrame(columns=self.data_frame.columns)
        # for error_level in range(self.filter_level, max_lever+1)[::-1]:
        #     error_level_cond = self.data_frame[self.right_level_columns] == error_level  # 当前正确等级
        #
        #     # 如果unique全部在case_df里面， 则不应该选取
        #     unique_cond = [True] * len(error_level_cond)
        #     for unique_key in self.unique_columns:
        #         unique_cond = unique_cond & self.data_frame[unique_key].isin(case_df[unique_key])
        #
        #     cond = error_level_cond & (~unique_cond)
        #
        #     case_df = case_df.append(self.data_frame[cond])
        return case_df
