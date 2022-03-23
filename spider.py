import sys
import time
import pymysql
import json
import traceback
import requests
import re
from bs4 import BeautifulSoup
import warnings

warnings.catch_warnings()

warnings.simplefilter("ignore")


def get_tencent_data():
    url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    url2 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    r1 = requests.get(url1, headers)
    r2 = requests.get(url2, headers)

    res1 = json.loads(r1.text)
    res2 = json.loads(r2.text)

    data_all1 = json.loads(res1["data"])
    data_all2 = json.loads(res2["data"])

    history = {}
    for i in data_all2["chinaDayList"]:
        ds = i["y"]+'.'+i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        nowConfirm = i["nowConfirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm,"nowConfirm": nowConfirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all2["chinaDayAddList"]:
        ds = i["y"]+'.'+i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirmadd = i["confirm"]
        suspectadd = i["suspect"]
        healadd = i["heal"]
        deadadd = i["dead"]
        history[ds].update({"confirm_add": confirmadd, "suspect_add": suspectadd,
                            "heal_add": healadd, "dead_add": deadadd})

    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])

    dayinfo = []
    day_time = data_all1["lastUpdateTime"]
    data_key = data_all2['provinceCompare'].keys()
    data_key = list(data_key)
    data_value = data_all2['provinceCompare'].values()
    data_value = list(data_value)
    for i in range(len(data_key)):
        city = data_key[i]
        now_confirm = data_value[i]['nowConfirm']
        confirm_add = data_value[i]['confirmAdd']
        heal = data_value[i]['heal']
        dead = data_value[i]['dead']
        zero = data_value[i]['zero']
        dayinfo.append([day_time, city, now_confirm, confirm_add, heal, dead, zero])


    return history, details,dayinfo





def get_conn():
    # 建立连接
    conn = pymysql.connect(host="localhost", user="root", password="root", db="cov", charset="utf8")
    # c创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


#定义更新细节函数
def update_details():
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]#1代表最新数据
        conn,cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        #对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新details数据")
            for item in li:
                cursor.execute(sql,item)
            conn.commit()
            print(f"{time.asctime()}details更新到最新数据")
        else:
            print(f"{time.asctime()}details已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


def update_dayinfo():
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[2]#1代表最新数据
        conn,cursor = get_conn()
        sql = "insert into dayinfo(day_time,city,now_confirm,confirm_add,heal,dead,zero) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select day_time from dayinfo order by id desc limit 1)'
        #对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新dayinfo数据")
            for item in li:
                cursor.execute(sql,item)
            conn.commit()
            print(f"{time.asctime()}dayinfo更新到最新数据")
        else:
            print(f"{time.asctime()}dayinfo已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


#插入历史数据
def insert_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]#0代表历史数据字典
        print(f"{time.asctime()}开始插入history数据")
        conn,cursor = get_conn()
        sql = 'insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for k,v in dic.items():
            cursor.execute(sql,[k,v.get('confirm'),v.get('confirm_add'),v.get('nowConfirm'),
                                v.get('suspect'),v.get('suspect_add'),v.get('heal'),
                                v.get('heal_add'),v.get('dead'),v.get('dead_add')])
        conn.commit()
        print(f"{time.asctime()}插入history数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


#更新历史数据
def update_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]#0代表历史数据字典
        print(f"{time.asctime()}开始更新history数据")
        conn,cursor = get_conn()
        sql = 'insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_query = 'select confirm from history where ds=%s'
        for k,v in dic.items():
            if not cursor.execute(sql_query,k):
                cursor.execute(sql, [k, v.get('confirm'), v.get('confirm_add'), v.get('nowConfirm'),
                                     v.get('suspect'), v.get('suspect_add'), v.get('heal'),
                                     v.get('heal_add'), v.get('dead'), v.get('dead_add')])
        conn.commit()
        print(f"{time.asctime()}history数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


#爬取新浪热搜数据
def get_sina_hot():
    from selenium.webdriver import Chrome, ChromeOptions
    import time

    option = ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')

    result = []
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    browser = Chrome(options=option)
    browser.get(url)
    time.sleep(10)
    content = browser.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a')
    count = 51

    for i in range(51):
        cont = content[i].text
        num = str(count - i)
        result.append(cont + num)
        #print(content[i].text)
    return result


def update_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_sina_hot()
        print(f"{time.asctime()}开始更新hotsearch数据")
        conn,cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql,(ts,i))
        conn.commit()
        print(f"{time.asctime()}hotsearch数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)

if __name__ == "__main__":
        update_history()
        update_details()
        update_dayinfo()
        update_hotsearch()
