#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 19-4-24 下午8:41
# @Email : jacobjzhang@tencent.com
# @File  : far_frr_example.py

"""拒识率, 误识别率计算"""

import pandas as pd
from calculator.far_frr_calculator import FARFRRCulator


def fake_data():
    columns = ['true_domain', 'pred_domain', 'unique_id']
    data_list = [
        ['other', 'video', 0],
        ['music', 'other', 1],
        ['music', 'music', 2],
        ['other', 'music', 3],
        ['other', 'music', 4]
        # ['other', 'video', 2],
        # ['other', 'fm', 3],
        # ['music', 'music', 4],
        # ['music', 'music', 5],
        # ['other', 'other', 6]
    ]
    df = pd.DataFrame(data=data_list, columns=columns)
    return df

def compare_data(df):
    def compare_func(row):
        true_domain, pred_domain = row['true_domain'], row['pred_domain']
        if true_domain == 'other' and pred_domain != 'other':
            return 1
        if true_domain == 'other' and pred_domain == 'other':
            return 2
        if true_domain != 'other' and pred_domain == 'other':
            return 1
        if true_domain != 'other' and pred_domain != 'other':
            return 2

    df['compare_result'] = df.apply(compare_func, axis=1)
    return df

def cal_far_frr(df):
    right_level_column = 'compare_result'
    label_columns = ['domain', ]
    unique_columns = ['unique_id', ]
    statistics_level = 'domain'
    agg_columns = ['domain', ]

    nlu_pr_handle = FARFRRCulator(
        right_level_column=right_level_column,
        data_frame=df,
        unique_columns=unique_columns,
        label_columns=label_columns,
        statistics_level=statistics_level,
        agg_columns=agg_columns,
    )

    cal_df, cal_case_df = nlu_pr_handle.cal()
    print '--' * 10, 'cal_far_frr',  '--' * 10
    print cal_df.head()
    print '----' * 20, '\n\n'
    print cal_case_df.head()

if __name__ == "__main__":
    df = fake_data()
    df = compare_data(df)
    cal_far_frr(df)