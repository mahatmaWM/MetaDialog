#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 18-12-26 下午4:56
# @Email : jacobjzhang@tencent.com
# @File  : nlu_pr_calculator.py

import pandas as pd
import numpy as np
from .calucator_based import CalculatorBased


# pd.options.mode.use_inf_as_na = True


class NluPRCalculator(object):
    def __init__(self,
                 right_level_column,
                 data_frame,
                 unique_columns,  # 表示哪些列是可以唯一标注语料（非语料对比关系）, 仅用来合并同一等级下对比结果相同的行。
                 label_columns,  # 表示那些列是预测和标注的, 必须严格按照正确level进行排序（domain, intent, slots）
                 statistics_level,  # 统计等级， 1～ len(lable_columns), 对应label_columns位置+1
                 agg_columns,  # 汇总结果时的列, 即结果呈现时的列
                 filter_level=None  # 统计时，需要过滤的等级
                 ):

        unique_columns = list(unique_columns)
        label_columns = list(label_columns)
        agg_columns = list(agg_columns)

        statistics_level = self.loc_statistics_level(statistics_level, label_columns)

        statistic_columns = label_columns[0: statistics_level]
        self.agg_columns = agg_columns

        self.precision_agg_columns = [
            'pred_' + column_name if 'pred_' + column_name in data_frame.columns else column_name
            for column_name in agg_columns]
        self.recall_agg_columns = ['true_' + column_name if 'true_' + column_name in data_frame.columns else column_name
                                   for column_name in agg_columns]

        self.recall_unique_columns = [
            'true_' + column_name if 'true_' + column_name in data_frame.columns else column_name
            for column_name in statistic_columns] + unique_columns
        self.precision_unique_columns = [
            'pred_' + column_name if 'pred_' + column_name in data_frame.columns else column_name
            for column_name in statistic_columns] + unique_columns

        # 聚合时, 应该按照聚合条件+唯一键进行去重
        self.recall_unique_columns = list(set(self.recall_unique_columns + self.recall_agg_columns))

        self.precision_unique_columns = list(set(self.precision_unique_columns + self.precision_agg_columns))

        self.right_level_column = right_level_column
        self.cut_right_level = statistics_level
        self.filter_level = statistics_level if not filter_level else filter_level
        self.data_frame = data_frame

    def loc_statistics_level(self, statistics_level, label_columns):
        """statistics_level可以传label_columns的数据"""
        index = [i for i, x in enumerate(label_columns) if x == statistics_level]
        if len(index) > 0:
            statistics_level = index[0] + 1
        else:
            statistics_level = statistics_level
        return statistics_level

    def cal_recall(self):
        assert self.recall_agg_columns, 'cal recall must have recall_agg_columns'
        assert self.recall_unique_columns, 'cal recall must have recall_unique_columns'
        tmp_columns = list(set(self.recall_agg_columns + self.recall_unique_columns + [self.right_level_column]))
        tmp_data_frame = self.data_frame[tmp_columns]
        calculator = CalculatorBased(statistics_columns=tuple(self.recall_agg_columns),
                                     unique_columns=tuple(self.recall_unique_columns),
                                     right_level_columns=self.right_level_column,
                                     cut_right_level=self.cut_right_level,
                                     # data_frame=self.data_frame,
                                     data_frame=tmp_data_frame,
                                     filter_level=self.filter_level)
        recall_df = calculator.cal()
        recall_df = recall_df.rename(columns={"wrong_num": "FN", "right_num": "TP"})
        recall_case_df = calculator.cal_case()
        recall_case_df['case_type'] = recall_case_df[self.right_level_column].apply(
            lambda x: 'TP' if x > self.cut_right_level else 'FN')
        recall_case_df = pd.merge(recall_case_df, self.data_frame, on=tmp_columns)

        recall_rename_dict = dict(zip(self.recall_agg_columns, self.agg_columns))
        recall_df = recall_df.rename(columns=recall_rename_dict)

        self.recall_df = recall_df
        # self.recall_df['recall'] = self.recall_df['TP'] / (self.recall_df['TP'] + self.recall_df['FN'])
        # self.recall_df['recall'] = np.divide(self.recall_df['TP'], self.recall_df['TP'] + self.recall_df['FN'])
        self.recall_df['recall'] = (1.0 * self.recall_df['TP']).div(
            (self.recall_df['TP'] + self.recall_df['FN']).where(
                (self.recall_df['TP'] + self.recall_df['FN']) != 0, np.nan
            )
        )

        self.recall_df = self.recall_df.fillna(0.0)
        self.recal_case_df = recall_case_df

        return recall_df, recall_case_df

    def cal_precision(self):
        assert self.precision_agg_columns, 'cal recall must have precision_agg_columns'
        assert self.precision_unique_columns, 'cal recall must have precision_unique_columns'
        tmp_columns = list(set(self.precision_agg_columns + self.precision_unique_columns + [self.right_level_column]))
        tmp_data_frame = self.data_frame[tmp_columns]

        calculator = CalculatorBased(statistics_columns=tuple(self.precision_agg_columns),
                                     unique_columns=tuple(self.precision_unique_columns),
                                     right_level_columns=self.right_level_column,
                                     cut_right_level=self.cut_right_level,
                                     # data_frame=self.data_frame,
                                     data_frame=tmp_data_frame,
                                     filter_level=self.filter_level)
        precision_df = calculator.cal()
        precision_df = precision_df.rename(columns={"wrong_num": "FP", "right_num": "TP"})
        precision_case_df = calculator.cal_case()
        precision_case_df['case_type'] = precision_case_df[self.right_level_column].apply(
            lambda x: 'TP' if x > self.cut_right_level else 'FP')

        precision_case_df = pd.merge(precision_case_df, self.data_frame, on=tmp_columns)

        precision_rename_dict = dict(zip(self.precision_agg_columns, self.agg_columns))
        precision_df = precision_df.rename(columns=precision_rename_dict)

        self.precision_df = precision_df
        # self.precision_df['precision'] = self.precision_df['TP'] / (self.precision_df['TP'] + self.precision_df['FP'])
        # self.precision_df['precision'] = np.divide(self.precision_df['TP'],
        #     self.precision_df['TP'] + self.precision_df['FP'])
        self.precision_df['precision'] = (self.precision_df['TP'] * 1.0).div(
            (self.precision_df['TP'] + self.precision_df['FP']).where(
                self.precision_df['TP'] + self.precision_df['FP'] != 0),
            np.nan
        )
        self.precision_df = self.precision_df.fillna(0.0)
        self.precision_case_df = precision_case_df

        return precision_df, precision_case_df

    def cal(self):
        precision_df, precision_case_df = self.cal_precision()
        recall_df, recall_case_df = self.cal_recall()

        cal_df = pd.merge(precision_df, recall_df,
                          on=self.agg_columns + ['TP'],
                          how='outer'
                          )

        fill_list = ['TP', 'FP', 'FN', 'precision', 'recall']
        for fill_column in fill_list:
            cal_df[fill_column] = cal_df[fill_column].fillna(0.0)

        cal_case_df = recall_case_df.append(precision_case_df)

        self.all_case_df = cal_case_df
        self.all_cal_df = cal_df

        self.all_cal_df['F1'] = 2 * self.all_cal_df['precision'] * self.all_cal_df['recall'] / \
                                (self.all_cal_df['precision'] + self.all_cal_df['recall'])
        self.all_cal_df['F1'] = self.all_cal_df['F1'].fillna(0.0)
        return cal_df, cal_case_df
