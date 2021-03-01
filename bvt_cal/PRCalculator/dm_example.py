#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from calculator.dm_prf_calculator import DMMetricsCal
from compare.compare_based import CompareBased


def example(df):
    # compare_columns = (('true_domain_name', 'pred_domain_name'),
    #                    ('true_intent_name', 'pred_intent_name'),
    #                    ('true_slots', 'pred_slots')
    #                    )

    label_columns = ('domain_name', 'intent_name', 'slots')

    unique_columns = ('corpus_id', )
    agg_columns = ('domain_name',)
    # compare_handle = CompareBased()

    compare_result = 'compare_result'
    # dataframe = compare_handle.compare(compare_columns=label_columns,
    #                                    data_frame=df, result_column=compare_result)

    dm_metrics_handle = DMMetricsCal(
        compare_result_column=compare_result,
        unique_columns=unique_columns,
        agg_columns=agg_columns,
        label_columns=label_columns,
    )

    final_metrics, final_case = dm_metrics_handle.cal(data_frame=df)
    return final_metrics, final_case


if __name__ == "__main__":
    import pandas as pd
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    # df = pd.read_excel('nlu_example.xlsx')
    df = pd.read_excel('merge_data.xlsx')
    final_metrics, final_case = example(df=df)
    final_metrics_all = final_metrics[final_metrics['level'] == 'all']
    print(final_metrics_all)
