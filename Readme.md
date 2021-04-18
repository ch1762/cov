# python 疫情可视化展示

## 项目已上线，详见8.140.27.208！

![fb6db3443afa8a6924b43e1e302e3cf](https://i.loli.net/2021/04/18/GhZCXdkNszp7x2i.png)

## 数据搜集

### 爬取腾讯数据

```python
import datetime
import json
import requests
from bs4 import BeautifulSoup
import time
### 封装函数 返回各省市疫情情况
def get_data():
    today = str(datetime.date.today())
    
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    res = requests.get(url)
    d = json.loads(res.text)
    data = json.loads(d['data'])
    province = data['provinceCompare']
    
    list1 = []
    for pro in province.keys():
        list1.append(pro)

    nowl = []
    for pro in province.values():
        nowl.append(pro['nowConfirm'])
        
    addl = []
    for pro in province.values():
        addl.append(pro['confirmAdd'])

    deadl = []
    for pro in province.values():
        deadl.append(pro['dead'])

    heall = []
    for pro in province.values():
        heall.append(pro['heal'])

    zerol = []
    for pro in province.values():
        zerol.append(pro['zero'])

    history = {}
    for d in data['chinaDayList']:
        tt = '2020.'+d['date']
        temp = time.strptime(tt,'%Y.%m.%d')
        tm = time.strftime('%Y-%m-%d',temp)
        confirm = d['confirm']#累计确诊
        dead = d['dead']#累计死亡
        heal = d['heal']#累计治愈
        suspect = d['suspect']#累计治愈
        nowConfirm = d['nowConfirm']#现存确诊
        history[tm] = {'confirm':confirm,'suspect':suspect,'heal':heal,'dead':dead,'nowConfirm':nowConfirm}
    for d in data['chinaDayAddList']:
        tt = '2020.'+d['date']
        temp = time.strptime(tt,'%Y.%m.%d')
        tm = time.strftime('%Y-%m-%d',temp)
        confirm = d['confirm']#新增确诊
        suspect = d['suspect']#新增疑似
        dead = d['dead']#新增死亡
        heal = d['heal']#新增治愈
        
    history[tm].update({'confirm_add':confirm,'suspect_add':suspect,'heal_add':heal,'dead_add':dead,'heal_add':heal})
    details = []
    for i in range(34):
        details.append([today,list1[i],nowl[i],addl[i],heall[i],deadl[i],zerol[i]])
    return history,details
```



###导入数据库

```python
import traceback
import pymysql
import datetime
import json
import requests
from bs4 import BeautifulSoup
import time

def get_conn():
    conn = pymysql.connect(host = '127.0.0.1',
                  user = 'root',
                  password ='root',
                  db = 'ch')
    cursor = conn.cursor()
    return conn,cursor
def close_conn(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        
def insert_history():
    '''
    插入history表
    '''
    cursor = None
    conn = None
    try:
        dic = get_data()[0]
        print(f'{datetime.datetime.now()} 开始插入历史数据')
        conn,cursor = get_conn()
        sql = 'insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for k,v in dic.items():
            cursor.execute(sql,[k,v.get('confirm'),v.get('suspect'),v.get('heal'),
                                v.get('dead'),v.get('nowConfirm'),v.get('confirm_add'),
                                v.get('suspect_add'),v.get('heal_add'),v.get('dead_add')])
        conn.commit()
        print(f'{datetime.datetime.now()} 历史数据插入完毕')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)
        
def update_history():
    '''
    更新history表
    '''
    cursor = None
    conn = None
    try:
        dic = get_data()[0]
        print(f'{datetime.datetime.now()} 开始更新历史数据')
        conn,cursor = get_conn()
        sql = 'insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_query = 'select confirm from history where dt=%s'
        for k,v in dic.items():
            if not cursor.execute(sql_query,k):
                cursor.execute(sql,[k,v.get('confirm'),v.get('suspect'),v.get('heal'),
                                    v.get('dead'),v.get('nowConfirm'),v.get('confirm_add'),
                                    v.get('suspect_add'),v.get('heal_add'),v.get('dead_add')])
        conn.commit()
        print(f'{datetime.datetime.now()} 历史数据更新完毕')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)
        
def update_details():
    '''
    更新details表
    '''
    cursor = None
    conn = None
    try:
        li = get_data()[1]
        conn,cursor = get_conn()
        sql = 'insert into details(update_time,province,now_confirm,confirm_add,heal_add,dead_add,zero_days) values(%s,%s,%s,%s,%s,%s,%s)'
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f'{datetime.datetime.now()} 开始更新数据')
            for item in li:
                cursor.execute(sql,item)
            conn.commit()
            print(f'{datetime.datetime.now()} 更新最新数据完毕')
        else:
            print(f'{datetime.datetime.now()} 已经是最新数据')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)
```

### 爬取新浪热搜数据

```python
def get_hotsearch():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    res = requests.get(url)
    html = res.text
    r = BeautifulSoup(html)
    s = r.find_all('a',attrs={'target':'_blank'})
    result = []
    for i in range(1,len(s)-10):
        pattern = '>(.*)</a>'
        text = re.search(pattern,str(s[i]))
        result.append(text.group(1)+str(50-i))
    return result
```

### 导入数据库

```python
import traceback
import pymysql
import datetime
import json
import requests
from bs4 import BeautifulSoup
import time

def update_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_hotsearch()
        print(f'{datetime.datetime.now()} 开始更新热搜数据')
        conn,cursor = get_conn()
        sql = 'insert into hotsearch(dt,content) values(%s,%s)'
        ts = time.strftime('%Y-%m-%d %X')
        for i in context:
            cursor.execute(sql,(ts,i))
        conn.commit()
        print(f'{datetime.datetime.now()} 数据更新完毕')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)
```

### 爬取网易当日疫情数据

```python
def get_daily():
    url = 'https://wp.m.163.com/163/page/news/virus_report/index.html?_nw_=1&_anw_=1'
    option = ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    browser = Chrome(options=option)
    browser.get(url)
    c = browser.find_elements_by_class_name('number')
    daily_data = []
    tm = time.strftime('%Y-%m-%d')
    daily_data.append(tm)
    for i in range(2,6):
        daily_data.append(c[i].text)
    return daily_data
```

### 导入数据库

```python
import time
import datetime
import traceback
from selenium.webdriver import Chrome,ChromeOptions
import pymysql


def update_daily():
    cursor = None
    conn = None
    try:
        context = get_daily()
        print(f'{datetime.datetime.now()} 开始更新当日数据')
        conn,cursor = get_conn()
        sql = 'insert into daily_data(time,now_confirm,confirm,dead,heal) values(%s,%s,%s,%s,%s)'
        cursor.execute(sql,[context[0],context[1],context[2],context[3],context[4]])
        conn.commit()
        print(f'{datetime.datetime.now()} 数据更新完毕')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)
```





