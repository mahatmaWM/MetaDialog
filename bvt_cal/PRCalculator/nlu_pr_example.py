#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 18-12-27 下午9:55
# @Email : jacobjzhang@tencent.com
# @File  : nlu_pr_example.py

import pandas as pd
from calculator.nlu_pr_calculator import NluPRCalculator


def app_key_domain():
    """按照app_key统计domain的指标"""
    data_frame = pd.read_excel('nlu_example.xlsx')
    right_level_column = 'compare_result'  # 指定正确等级的列名
    label_columns = ['domain_name', 'intent_name', 'slots']  # 指定true, pred列名(脱敏于true_**, pred_**)
    unique_columns = ['corpus_id']   # 可唯一代表数据的列名（数据可存在多行, 表示多组true, pred关系）
    statistics_level = 'domain_name'   # 正确等级大于3为正确, 小于3为错误。此处代表统计domain指标
    agg_columns = ['app_key']  # 聚合列名, app_Key统计的指标

    nlu_pr_handle = NluPRCalculator(
        right_level_column=right_level_column,
        data_frame=data_frame,
        unique_columns=unique_columns,
        label_columns=label_columns,
        statistics_level=statistics_level,
        agg_columns=agg_columns,
    )

    cal_df, cal_case_df = nlu_pr_handle.cal()
    print '--' * 10, 'app_key_domain',  '--' * 10
    print cal_df.head()
    print '----' * 20, '\n\n'


def domain_slots():
    """按照domain统计slots的指标"""
    data_frame = pd.read_excel('nlu_example.xlsx')
    right_level_column = 'compare_result'  # 指定正确等级的列名
    label_columns = ['domain_name', 'intent_name', 'slots']  # 指定true, pred列名(脱敏于true_**, pred_**)
    unique_columns = ['corpus_id']   # 可唯一代表数据的列名（数据可存在多行, 表示多组true, pred关系）
    statistics_level = 3             # 正确等级大于3为正确, 小于3为错误。此处代表统计参数指标
    agg_columns = ['domain_name']    # 聚合列名, app_Key统计的指标(脱敏于true_**, pred_**)

    nlu_pr_handle = NluPRCalculator(
        right_level_column=right_level_column,
        data_frame=data_frame,
        unique_columns=unique_columns,
        label_columns=label_columns,
        statistics_level=statistics_level,
        agg_columns=agg_columns,
    )

    cal_df, cal_case_df = nlu_pr_handle.cal()
    print '--' * 10, 'domain_slots', '--' * 10
    print cal_df.head()
    print '----' * 20, '\n\n'


def app_key_domain_intent():
    """按照app_key + domain统计intent的指标"""
    data_frame = pd.read_excel('nlu_example.xlsx')
    right_level_column = 'compare_result'  # 指定正确等级的列名
    label_columns = ['domain_name', 'intent_name', 'slots']  # 指定true, pred列名(脱敏于true_**, pred_**)
    unique_columns = ['corpus_id']   # 可唯一代表数据的列名（数据可存在多行, 表示多组true, pred关系）
    statistics_level = 2             # 正确等级大于3为正确, 小于3为错误。此处代表统计intent指标
    agg_columns = ['app_key', 'domain_name']    # 聚合列名, app_Key统计的指标(脱敏于true_**, pred_**)

    nlu_pr_handle = NluPRCalculator(
        right_level_column=right_level_column,
        data_frame=data_frame,
        unique_columns=unique_columns,
        label_columns=label_columns,
        statistics_level=statistics_level,
        agg_columns=agg_columns,
    )

    cal_df, cal_case_df = nlu_pr_handle.cal()
    print '--' * 10, 'app_key_domain_intent', '--' * 10
    cal_df = cal_df.sort_values(by=['domain_name'])
    print cal_df.head()
    print '----' * 20, '\n\n'
    print cal_case_df.head()


def main():
    app_key_domain()
    # domain_slots()
    app_key_domain_intent()

if __name__ == "__main__":
    main()


