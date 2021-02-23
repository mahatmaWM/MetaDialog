#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 19-4-24 下午9:21
# @Email : jacobjzhang@tencent.com
# @File  : far_frr_calculator.py
"""
拒识率、误识率计算

拒识率= sum(true_domain & fake_other) / sum(true_domain)
误识率= sum(true_other & fake_domain) / sum(true_other)

"""
import pandas as pd
from .nlu_pr_calculator import NluPRCalculator


def fa_far_frr_case_type(data_dict):
    # for key in data_dict:
    #     # if key.startswith('true_domain'):
    #     #     true_domain = data_dict[key]
    #     if key.startswith('pred_domain'):
    #         pred_domain = data_dict[key]
    case_type = data_dict['case_type']
    if  case_type == 'FP':
        data_dict['case_type'] = 'FA'
    else:
        data_dict['case_type'] = 'RIGHT'
    return data_dict

def fr_far_frr_case_type(data_dict):
    # for key in data_dict:
    #     # if key.startswith('true_domain'):
    #     #     true_domain = data_dict[key]
    #     if key.startswith('pred_domain'):
    #         pred_domain = data_dict[key]
    case_type = data_dict['case_type']
    if  case_type == 'FN':
        data_dict['case_type'] = 'FR'
    else:
        data_dict['case_type'] = 'RIGHT'
    return data_dict


class FARFRRCulator(NluPRCalculator):
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
        super(FARFRRCulator, self).__init__(right_level_column=right_level_column,
                                            data_frame=data_frame,
                                            unique_columns=tuple(unique_columns),
                                            label_columns=tuple(label_columns),
                                            statistics_level=statistics_level,
                                            agg_columns=tuple(agg_columns),
                                            filter_level=filter_level)
        # self.agg_columns =

    def cal(self):
        # cal_df, cal_case_df = super(FARFRRCulator, self).cal()
        recall_cal_df, recall_cal_case_df = self.cal_recall()
        precision_cal_df, precision_cal_case_df = self.cal_precision()
        # remain_columns = [column for column in recall_cal_df.columns if column not in self.agg_columns]
        # remain_columns.append('domain_name')
        # tmp_recall_df = recall_cal_df[remain_columns].drop_duplicates(subset=remain_columns)

        # tmp_other_df = tmp_recall_df[tmp_recall_df['domain_name'] == 'other']

        # tmp_other_df = tmp_other_df.drop_duplicates(subset=['domain_name', 'TP', 'FN'])
        # print tmp_other_df
        # print self.agg_columns
        # print recall_cal_df.columns
        # print(self.agg_columns)
        # print(len(recall_cal_df.drop_duplicates(subset=list(self.agg_columns))))

        tmp_df = recall_cal_df
        tmp_df = recall_cal_df[recall_cal_df['domain_name'] == 'other']
        agg_columns = list(self.agg_columns)
        agg_columns.remove('domain_name')
        tmp_df = tmp_df.drop_duplicates(subset=agg_columns)
        tmp_df1 = tmp_df.groupby(agg_columns)['TP'].sum().reset_index(name='other1')
        tmp_df2 = tmp_df.groupby(agg_columns)['FN'].sum().reset_index(name='other2')
        all_other_df = pd.merge(left=tmp_df1, right=tmp_df2, on=agg_columns)
        # print(tmp_df3)
        # print(tmp_df1)
        all_other_df['all_other'] = all_other_df['other1'] + all_other_df['other2']
        columns = list(all_other_df.columns)
        columns.remove('other1')
        columns.remove('other2')

        # assert len(tmp_other_df) <=1, 'other length must <=1, length is %s' % (len(tmp_other_df))
        # all_other = recall_cal_df[recall_cal_df['domain_name'] == 'other']['TP'].sum()
        # all_other += recall_cal_df[recall_cal_df['domain_name'] == 'other']['FN'].sum()
        # metrics = pd.DataFrame()
        recall_cal_df['FR'] = recall_cal_df['FN']
        recall_cal_df['RIGHT'] = recall_cal_df['TP']
        precision_cal_df['FA'] = precision_cal_df['FP']


        precision_cal_case_df = pd.DataFrame(map(fa_far_frr_case_type, precision_cal_case_df.to_dict(orient='index').values()))
        recall_cal_case_df = pd.DataFrame(map(fr_far_frr_case_type, recall_cal_case_df.to_dict(orient='index').values()))
        cal_case_df = precision_cal_case_df.append(recall_cal_case_df)

        metrics = pd.merge(recall_cal_df, precision_cal_df,
                           on=self.agg_columns,
                           how='outer'
                           )
        metrics = pd.merge(left=metrics, right=all_other_df, on=agg_columns, how='outer')
        metrics = metrics.fillna(0.0)
        metrics['far'] = metrics['FA'] * 1.0 / metrics['all_other']
        metrics['frr'] = metrics['FR'] * 1.0 / (metrics['RIGHT'] + metrics['FR'])
        metrics = metrics.fillna(0.0)
        # metrics['all_other'] = all_other

        return metrics, cal_case_df


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_excel(u'/home/jacobjzhang/zj/Project/PRCalculator/已完成_新2019-12-22-925全双工-线上评测.xlsx')


    # print df.head()

    def trans(data_dict):
        data_dict['pred_domain'] = 'other' if data_dict['domain'] == 'default' else data_dict['domain']

        data_dict['true_domain'] = 'other' if data_dict['label_domain'] == 'default' else data_dict['label_domain']
        return data_dict


    def error_type(data_dict):
        if data_dict['pred_domain'] == data_dict['true_domain']:
            data_dict['error_type'] = 2
        elif data_dict['pred_domain'] != 'other' and data_dict['true_domain'] != 'other':
            data_dict['error_type'] = 2
        else:
            data_dict['error_type'] = 1
        return data_dict


    df = pd.DataFrame(map(trans, df.to_dict(orient='index').values()))
    df = pd.DataFrame(map(error_type, df.to_dict(orient='index').values()))
    df['comb_id'] = range(0, len(df))
    ret_codes = [0, -3]
    df["is_duplex"] = df["is_duplex"].map(lambda x: x.strip())
    df = df[df["ret_code"].isin(ret_codes) & (df['is_duplex'] == 'true')]
    # df.to_excel('hah.xlsx')
    df['pred_domain_name'] = df['pred_domain']
    df['true_domain_name'] = df['true_domain']
    handle = FARFRRCulator(
        right_level_column='error_type',
        data_frame=df,
        unique_columns=['comb_id', ],  # 表示哪些列是可以唯一标注语料（非语料对比关系）, 仅用来合并同一等级下对比结果相同的行。
        label_columns=['domain_name', ],  # 表示那些列是预测和标注的, 必须严格按照正确level进行排序（domain, intent, slots）
        statistics_level=1,  # 统计等级， 1～ len(lable_columns), 对应label_columns位置+1
        agg_columns=['domain_name', ],  # 汇总结果时的列, 即结果呈现时的列
        filter_level=None  # 统计时，需要过滤的等级
    )
    cal_df, cal_case_df = handle.cal()
    # print cal_df
    # print cal_case_df.columns
    # print cal_case_df.to_excel('cal_case_df.xlsx')
    # print cal_df
    # print cal_df.columns
    # print cal_case_df.columns
    cal_df.to_excel('cal_df.xlsx')
    cal_case_df.to_excel('cal_case_df.xlsx')