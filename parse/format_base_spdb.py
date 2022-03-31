#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名: format_base_spdb.py
# 作者:WangXu
# 联系邮箱:iswongx@163.com

# 格式化基本信息
import random
import re
import uuid
import requests
import time
from to_sql import save_data_to_sql
from redis_client import redis_connect
import json
import urllib3
from spider import Spider_data
from settings import ua
from settings import code_new

urllib3.disable_warnings()

conn = redis_connect.Redis_connect()



# 获取真实页面方法
def get_true(url,session):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': session,
        'user-agent': random.choice(ua.get('user_agent')),
    }
    print('=============================当前正在进入：{} ===================================='.format(url))
    try:
        res = requests.get(url, headers=headers, timeout=20, verify=False)
        time.sleep(0.5)
        if res.status_code == 200:
            info = res.text
            char = re.findall('charset="{0,1}(.*?)"', info, re.S)
            if char:
                try:
                    info1 = res.content.decode(encoding='{}'.format(char[0].lower()))
                    return info1, res.url
                except Exception as e:
                    print(e, '异常编码了================')
                    return info, res.url
            else:
                # logging_.info('编码异常-连接为{}，'.format(res.url))
                return '编码异常', res.url
        else:
            print('状态码异常返回数据', res.text)
            # logging_.info('状态码/服务异常-被访问链接为{}，'.format(res.url))
            return '服务异常', res.url
    except Exception as e:
        print(e, '异常')
        headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'If-None-Natch': '',
            'If-Modified-Since': '',
            'user-agent': random.choice(ua.get('user_agent'))
        }
        print('进入重定向了======1111 主意呀=========')
        try:
            res = session.get(url, headers=headers1, timeout=20, verify=False)
            # logging_.info('特殊异常{}，异常连接{}'.format(e, url))
            return res.text, url
        except Exception as e:
            print(e, '---------')
            return '超时', url


# 详情页解析
def format_data(data, dict,dict_details):

    # 作者名称
    author2 = re.findall('<meta property="og:article:author" content="(.*?)"/>', data, re.S)
    if author2:
        author = author2[0].replace('\n', '').strip()
        dict_details['author'] = author.strip()
    else:
        author3 = re.findall('<strong class="profile_nickname">(.*?)</strong>', data, re.S)
        if author3:
            dict_details['author'] = author3[0].replace('\n', '').strip()
        else:
            dict_details['author'] = ''

    # 主角(默认为空)
    protagonist = ''
    if '主角' in data:
        protagonist = re.findall('主角：(.*?)<', data)
        if protagonist:
            dict_details['protagonist'] = protagonist[0].strip()
        else:
            dict_details['protagonist'] = ''
    else:
        dict_details['protagonist'] = protagonist
    # 小说简介
    if '小说介绍' in data:
        new_str = data[data.find('小说介绍'):data.find('长按识别开始看')]
        comp = re.compile(r'<[^>]+>')
        str = re.sub(comp, '', new_str).replace('小说介绍', '').replace('\n', '').replace('↓', '').strip()
        dict_details['describe'] = str
    else:
        stri = re.findall('<div class="rich_media_content " id="js_content" style="visibility: hidden;">(.*?)</div>',
                          data, re.S)
        if stri:
            comp = re.compile(r'<[^>]+>')
            str = re.sub(comp, '', stri[0]).replace('&nbsp;', '').strip()
            if '小说简介' in str:
                new_str = str[str.find('小说简介')::].replace('小说简介', '').strip()
                dict_details['describe'] = new_str
            else:
                dict_details['describe'] = str

    # 章节标题
    tittle = re.findall('<h1 class="rich_media_title" id="activity-name">(.*?)</h1>', data, re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].replace('\n','').strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details


# 首页数据解析
def format_text(first_data_list, tittle_list, keyword,cookies,list_redis,section_name, author):
    cookies1 = cookies
    for i, n in zip(first_data_list, tittle_list):
        number = str(uuid.uuid1()).replace('-', '')
        dict = {}
        if 'http:' in i:
            i = i
        else:
            i = 'https://weixin.sogou.com' + i

        n = n.replace('&rdquo;', '').replace('red', '').replace('beg', '').replace('<em>', '').replace('end',
                                                                                                       '').replace(
            '&ldquo;', '').replace(
            '<!--_-->', '').replace('\r\n', '').replace('</em>','').strip()

        # 更进一步解析获取的脏数据
        new_url = i
        dict['number'] = number
        dict['tittle'] = n
        # 跳转链接
        dict['url'] = new_url
        # 真实链接
        dict['true_url'] = ''
        dict['keyword'] = keyword
        dict['cookies'] = cookies1
        dict['section_name'] = section_name
        dict['author_name'] = author
        list_redis.append(dict)


# 获取jsessionid
def get_jsessionid():
    url = 'https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp'
    headers = {
        'user-agent': random.choice(ua.get('user_agent'))
    }
    resss = requests.get(url, headers=headers)
    cookie = ''
    for k, v in resss.cookies.items():
        cookie = cookie + k + '=' + v + ';'
    return cookie


# 搜狗获取真是链接程序
def get_sougou_weixin_rue_url(skip_url,session):
    headers = {
        'Cookie': session,
        'Host': 'weixin.sogou.com',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(ua.get('user_agent'))
    }
    try:
        res = requests.get(skip_url, headers=headers, verify=False)
        if res.status_code == 200:
            data = res.content.decode('utf-8')
            data1 = re.findall("url \+=.*?'(.*?)';", data, re.S)
            if data1:
                new_url = ''.join(data1)
                print(new_url, '真实链接==1kokofklsflsk')
                return new_url
            else:
                data2 = res.text
                print(res.text,'000999999999999911111111111111111111111111')
                data3 = re.findall("url \+=.*?'(.*?)';", data2, re.S)
                if data3:
                    new_url3 = ''.join(data3)
                    print(new_url3, '真实链接==')
                    return new_url3
                else:
                    print(res.text)
                    print('1111111111111111111111111111111111111111111111 ')
        else:
            print(res.text)
            print('99999999999999999999999')
    except Exception as e:
        print(e, '真实连接')
        res = requests.get(skip_url, headers=headers, verify=False)
        if res.status_code == 200:
            info = res.text
            data1 = re.findall("URL='(.*?)'", info)
            if data1:
                return data1[0]
        return skip_url


# 解析规则
def parse_html_to_str(htmlbody):
    # 去除页面中所有的 script 标签
    re_script = re.compile('<script[^>]*>[\s\S]*?<\/script>', re.I)
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # 去除页面中的style 标签
    del_label = re.compile(r'<[^>]+>', re.S)  # 去除页面中所有的标签

    content_del = re_script.sub("", htmlbody)
    content_del = re_style.sub("", content_del)
    content_del = del_label.sub("", content_del)
    # 去除标签后 会出现很多的空格 或者 换行符 ，对其进行处理
    content_del = content_del.replace('\t', '').replace(' ', '')
    # 处理后发现 有很多的空行，按 换行符进行分割
    content_del = content_del.split('\n')
    content = ''
    # 处理空行
    for c in content_del:
        if c:
            content = content + c.strip() + '\n'
    # 去除所有空格
    new_1 = re.sub('\s+', '', content)
    # 循环去除特殊符号
    for i in code_new:
        new_1 = new_1.replace('{}'.format(i), '')
    return new_1


# 主要解析程序
def get_(new_keyword, new_tittle, details_data, true_url,
                          dict,number):
    book_dict = {}
    new_dict = {}
    sql_server = save_data_to_sql.Save_score_to_sql()
    # 解析详情页数据
    book_dict['number'] = number
    book_dict['book_name'] = new_keyword
    book_dict['true_url'] = true_url
    book_html = parse_html_to_str(htmlbody=details_data)
    book_name = dict['keyword']
    book_author = dict['author_name']
    book_section = dict['section_name']
    book_dict['book_detail'] = book_html
    name_score = 0.0
    if book_name in book_html:
        name_score = name_score + 1.0
        new_dict['book_name_score'] = name_score
    else:
        new_dict['book_name_score'] = 0.0
    book_author_ = 0.0
    if book_author in book_html:
        book_author_ = book_author_ + 1.0
        new_dict['author_score'] = book_author_
    else:
        new_dict['author_score'] = 0.0

    section_list = book_section.split(';')
    sec_score = 0.0
    for sec in section_list:
        if sec in book_html:
            sec_score = sec_score + 0.2
    new_dict['section_score'] = sec_score
    new_dict['weight'] = name_score + book_author_ + sec_score
    # 详情整页数据存储
    sql_server.book_html_to_sql(data=book_dict)
    if new_keyword in new_tittle:
        if details_data == '编码异常':
            print('编码异常====', true_url)
            return None
        if details_data == '超时':
            print('超时了------------------', true_url)
            return None
        if details_data == '服务异常':
            print('服务异常=================', true_url)
            return None

        format_data(data=details_data, dict=dict,dict_details=new_dict)
        # 数据库存放数据
        sql_server = save_data_to_sql.Save_score_to_sql()
        sql_server.search_data_to_sql(data=dict)
        sql_server.details_data_to_sql(data=dict)

    else:
        print('不符合跳过0000000000000000000000000000000000')
        print(new_tittle, '111111111111111111')
        print(true_url, '2222222222222222')
