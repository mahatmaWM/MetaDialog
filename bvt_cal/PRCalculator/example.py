#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 18-12-25 下午2:34
# @Email : jacobjzhang@tencent.com
# @File  : example.py
import time

from load_data import *
from online_data_format import format
from compare.compare_based import CompareBased
from calculator.nlu_pr_calculator import NluPRCalculator

data = load_data_by_json()
# data = load_data()

print(len(data))
df = format(data)

compare_columns = [['true_domain_name', 'pred_domain_name'],
                   ['true_intent_name', 'pred_intent_name'],
                   ['true_slots', 'pred_slots']
                   ]

compare_handle = CompareBased(compare_columns_pairs=compare_columns,
                              data_frame=df)

compare_result = 'compare_result'
dataframe = compare_handle.compare(result_column=compare_result)
dataframe.to_excel('example.xlsx')

label_columns = ['domain_name', 'intent_name', 'slots']

unique_columns = ['corpus_id']   # 统计时的合并列

nlu_pr_handle = NluPRCalculator(
    right_level_column=compare_result,
    data_frame=dataframe,
    unique_columns=unique_columns,
    label_columns=label_columns,
    statistics_level=3,
    agg_columns=['sampling_type', 'app_key'],
)


cal_df, cal_case_df = nlu_pr_handle.cal()
print(cal_df)
print('--' * 20)
a = [1, 2, 3]
index = [i for i, x in enumerate(a) if x == 1]
print(index)
