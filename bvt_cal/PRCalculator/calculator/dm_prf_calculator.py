import pandas as pd
from .nlu_pr_calculator import NluPRCalculator


class DMMetricsCal(object):
    def __init__(self,
                 compare_result_column=None,
                 unique_columns=None,
                 agg_columns=None,
                 label_columns=None
                 ):
        self.compare_result_column = compare_result_column
        self.label_columns = ('domain_name_compliant',
                              'intent_name_compliant',
                              'slots_compliant') if label_columns is None else label_columns
        self.unique_columns = ('log_id',) if unique_columns is None else unique_columns
        self.agg_columns = ('domain_name_compliant',) if agg_columns is None else agg_columns

    def _cal_unit(self, data_frame, statistics_level, filter_level=None, level_tag='domain'):
        nlu_pr_handle = NluPRCalculator(
            right_level_column=self.compare_result_column,
            data_frame=data_frame,
            unique_columns=self.unique_columns,
            label_columns=self.label_columns,
            statistics_level=statistics_level,
            agg_columns=self.agg_columns,
            filter_level=filter_level
        )
        cal_df, cal_case_df = nlu_pr_handle.cal()
        cal_df['level'] = level_tag
        cal_case_df['level'] = level_tag
        return cal_df, cal_case_df

    def cal_nlu_data(self, data_frame):
        domain_metrics, domain_case_df = self._cal_unit(data_frame=data_frame, statistics_level=self.label_columns[0],
                                                        level_tag='domain')
        intent_metrics, intent_case_df = self._cal_unit(data_frame=data_frame, statistics_level=self.label_columns[1],
                                                        level_tag='intent')
        slots_metrics, slots_case_df = self._cal_unit(data_frame=data_frame, statistics_level=self.label_columns[2],
                                                      level_tag='slots')
        all_metrics, all_case_df = self._cal_unit(data_frame=data_frame,
                                                  statistics_level=self.label_columns[2],
                                                  filter_level=-1,
                                                  level_tag='all'
                                                  )
        core_metrics, core_case_df = self._cal_unit(data_frame=data_frame,
                                                    statistics_level=self.label_columns[1],
                                                    filter_level=-1,
                                                    level_tag='core'
                                                    )
        final_metrics = pd.concat([domain_metrics,
                                   intent_metrics,
                                   slots_metrics,
                                   all_metrics,
                                   core_metrics])
        final_case = pd.concat([
            domain_case_df,
            intent_case_df,
            slots_case_df,
            all_case_df,
            core_case_df
        ])
        return final_metrics, final_case

    def cal(self, data_frame):
        # df = BaseFormat.format(df=df)
        # df = self.before_process(df=df)
        # df = self.compare(df=df)
        final_metrics, final_case = self.cal_nlu_data(data_frame=data_frame)
        return final_metrics, final_case
