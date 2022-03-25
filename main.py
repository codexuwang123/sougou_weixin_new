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
from multiprocessing import Pool
import threading

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

                spider_self = Spider_data.Spider_desc_sougou(wd=i.get('Search_Keyword'))
                spider_self.spider_sougou(pn=n, keyword=spider_self.wd)

        # 更新爬虫状态
        s_data.undate_data(status_='1', keyword=i.get('Search_Keyword'))
        # 关闭数据库连接
        # s_data.close()
        return keyword_list
    else:
        print('========温馨提示：没有有效关键词需要爬取=======')


if __name__ == '__main__':

    keyword_list = last_mains()
    num = 4
    p = Pool(num)
    red = redis_connect.Redis_connect()
    flag = True
    while flag:
        print('等待新任务中========')
        try:
            flag_data = red.search_all_data(redis_key='sougou')
            flags = len(flag_data)
            red = redis_connect.Redis_connect()
            get_ = format_base_spdb.get_
            # 最大任务数
            process_num = flags
            for i in range(process_num):
                p.apply_async(get_, args=())
            p.close()
            p.join()
            if len(flag_data) == 0:
                for k in keyword_list:
                    s_data.undate_data(status_='2', keyword=k.get('Search_Keyword'))
        except Exception as e:
            print(e,'=============')
        time.sleep(3)
