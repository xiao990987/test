# ! /usr/bin/python
# -*- coding: utf-8 -*-
# author:凌
# datetime:2020/10/04 22:01
# software:PyCharm

import requests
import re
import time, random
from multiprocessing.dummy import Pool as ThreadPool
from fake_useragent import UserAgent


# 百度相关关键词查询
def xgss(url):
    sjs = random.randint(111111, 999999)
    #print(sjs)
    sj = str(sjs)
    ua = UserAgent()
    headers = {
        'Cookie': 'BIDUPSID=A484BA501E92BE1CA6537C00F7155E36; PSTM=1558489515; BAIDUID=75912F7E3DD9AB678D8B98EEE8D263DE:FG=1; BD_UPN=12314353; H_PS_PSSID=; H_PS_645EC=a0f4GSgzx44WxF1PZV01LZFmAyUbaDsJJ882KRllgCkTAGrK0tV0eXNoXakEyZNGUxuz5Xgf2qs; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; COOKIE_SESSION=341509_0_9_6_5_45_0_3_9_7_1_41_0_0_0_0_1564971440_0_1578376068%7C9%230_0_1578376068%7C1; delPer=0; BD_CK_SAM=1; PSINO=6; BDSVRTM=526',
        'Referer': 'https://www.baidu.com/?tn=4%s1_6_hao_pg' % sj,
        "User-Agent": ua.random
        # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    html = requests.get(url, headers=headers).content.decode('utf-8')
    time.sleep(2)
    # print(html)
    ze = r'<div id="rs"><div class="new-pmd"><div class="tt.+?">相关搜索</div><table class="new-inc-rs-table" cellpadding="0">(.+?)</table></div>'
    xgss = re.findall(ze, html, re.S)
    # print(xgss)
    xgze = r'<th><a class="c-font-medium" href="(.+?)">(.+?)</a></th>'
    sj = re.findall(xgze, str(xgss), re.S)
    # print(sj)
    gjc_lst = []
    i = 0
    for x in sj:
        print(x[1])
        # gjc = gjc + x[1] + '\n'
        if i < 3:
            gjc_lst.append(x[1])

        i = i + 1
    gjc = "_".join(gjc_lst)

    # 导出关键词为txt文本
    with open(".\gjcsj.txt", 'a', encoding='utf-8') as f:
        f.write(gjc+"\n")
    print("-----------------------------------")
    return gjc


print('\n========================工具说明========================')
print('百度相关关键词挖掘采集工具-by huguo002\n')
print('1.gjc.txt 为搜索词来源文件，关键词一行一个，最后一个关键词后须换行；')
print('2.gjcsj.txt 为输出关键词保存文档；')
print('注意，大批量采集使用容易和谐！\n')
print('================= BUG 反馈微信：huguo00289 ============\n')
time.sleep(5)
print("程序运行，正在导入关键词列表！！！")
#print("-----------------------------------")

# 导入要搜索的关键词txt列表
urls = []
data = []
for line in open('.\gjc.txt', "r", encoding='utf-8'):
    if line != '\n':
        data.append(line)
print("导入关键词列表成功！")
print("-----------------------------------")

# 转换关键词为搜索链接
for keyword in data:
    url = 'https://www.baidu.com/s?wd=' + keyword
    urls.append(url)

print("采集百度相关搜索关键词开启！")
print("...................")
# 多线程获取相关关键词
try:
    # 开4个 worker，没有参数时默认是 cpu 的核心数
    pool = ThreadPool()
    results = pool.map(xgss, urls)
    pool.close()
    pool.join()
    print("采集百度相关搜索关键词完成，已保存于gjcsj.txt！")
except:
    print("Error: unable to start thread")

print("8s后程序自动关闭！！！")
time.sleep(8)
