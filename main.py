#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:settings.py
# 创建日期:2022/3/10 10:19
# 作者:XU
# 联系邮箱:iswongx@163.com

import time
from to_sql import save_data_to_sql
from spider import Spider_data
from parse import format_base_spdb
from redis_client import redis_connect
from concurrent.futures import ThreadPoolExecutor
import uuid
import json
from parse import format_base_spdb
from settings import set_

conn = redis_connect.Redis_connect()
# 实例化sql链接
s_data = save_data_to_sql.Save_score_to_sql()


# 主函数调用
def last_mains():
    # 数据库获取关键次列表
    keyword_list = s_data.get_keyword()
    if keyword_list:
        i = ''
        for i in keyword_list:
            for n in range(1, 6):
                spider_self = Spider_data.Spider_desc_sougou_weixin(wd=i.get('Search_Keyword'))
                spider_self.spider_sougou_weixin(page=n, keyword=spider_self.wd)

        # 更新爬虫状态
        s_data.undate_data(status_='1', keyword=i.get('Search_Keyword'))
        # 关闭数据库连接
        # s_data.close()
        return keyword_list
    else:
        print('========温馨提示：没有有效关键词需要爬取=======')


# 总调用
def main_parse(dict):
    print('线程进来了================')
    new_tittle = dict.get('tittle')
    new_url = dict.get('url')
    cookies = dict.get('cookies')
    cookies1 = format_base_spdb.get_jsessionid()
    print(type(new_url), new_url, '000000011111111111111111111111111')
    true_url1 = format_base_spdb.get_sougou_weixin_rue_url(skip_url=new_url, session=cookies + cookies1)
    details_data, true_url = format_base_spdb.get_true(url=true_url1, session=cookies + cookies1)
    dict['true_url'] = true_url
    new_keyword = dict.get('keyword')
    number = str(uuid.uuid1()).replace('-', '')
    dict['number'] = number
    format_base_spdb.get_(new_keyword=new_keyword, new_tittle=new_tittle, details_data=details_data,
                          true_url=true_url,
                          dict=dict)


if __name__ == '__main__':

    while True:
        print('等待新任务中========')
        try:
            conn = redis_connect.Redis_connect()
            flag_data = conn.search_all_data(redis_key='sougou_weixin')
            flags = len(flag_data)
            if flags == 0:
                continue
            else:
                # 实例化sql链接
                dta = conn.search_data_redis(redis_key='sougou_weixin')
                dict = json.loads(dta)
                book_name = dict.get('book_name')
                data_book = dict.get('data')
                # 最大任务数
                with ThreadPoolExecutor(max_workers=set_.get('max_workers')) as f:

                    results = f.map(main_parse, data_book)

                s_data.undate_data(status_='2', keyword=book_name)

        except Exception as e:
            print(e, '=============')
        time.sleep(3)
