#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from PRCalculator.calculator.dm_prf_calculator import DMMetricsCal
from PRCalculator.compare.compare_based import CompareBased


def example(df):
    # compare_columns = (('true_domain_name', 'pred_domain_name'),
    #                    ('true_intent_name', 'pred_intent_name'),
    #                    ('true_slots', 'pred_slots')
    #                    )

    label_columns = ('domain_name', 'intent_name', 'slots')

    unique_columns = ('corpus_id', )
    agg_columns = ('app_key', 'domain_name')
    compare_handle = CompareBased()

    compare_result = 'compare_result'
    dataframe = compare_handle.compare(compare_columns=label_columns,
                                       data_frame=df, result_column=compare_result)

    dm_metrics_handle = DMMetricsCal(
        compare_result_column=compare_result,
        unique_columns=unique_columns,
        agg_columns=agg_columns,
        label_columns=label_columns,
    )

    final_metrics, final_case, ori_df = dm_metrics_handle.cal(df=dataframe)
    return final_metrics, final_case, ori_df

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_excel('nlu_example.xlsx')
    final_metrics, final_case, ori_df = example(df=df)
    print(final_metrics.head())
