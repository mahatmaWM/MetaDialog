#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: jacobjzhang
# @Time  : 18-12-21 下午8:44
# @Email : jacobjzhang@tencent.com
# @File  : load_data.py

import db
import json


def load_data(sampling_type=2):
    dop_online_database = db.DatabaseUtils(db.db_config.tag_db_dic)
    dop_online_database.open_database()

    select_sql = (" select id, session_id, corpus_content, dm_multi_di, tag_multi_di, datetime, current_scene"
                  " from dobby_platform_online_aiproxy "
                  " where ds=20181225 "
                  " and sampling_type = {sampling_type}" 
                  " and tag_multi_di like '%[%' "
                  " and app_key='2b82efec-a77c-46cd-a2c2-8df9bbd1d1c3'"
                  # " and (tag_multi_di like '%navigation_map%' or dm_multi_di like '%navigation_map%')"
                  "").format(sampling_type=sampling_type)

    results = dop_online_database.query_sql_execute(select_sql)
    # with open('20181219.json', 'w') as handle:
        # json.dump(results, handle)
    return results

def load_data_by_json():
    with open('20181219_all.json', 'r') as handle:
        tmp_result = json.load(handle)
    return tmp_result