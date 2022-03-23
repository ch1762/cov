# python 疫情可视化展示

## 项目已上线，详见http://60.205.169.29/ ！（又下线了！T_T）

![fb6db3443afa8a6924b43e1e302e3cf](https://i.loli.net/2021/04/18/GhZCXdkNszp7x2i.png)

## 数据搜集

### 爬取腾讯疫情数据

```python
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
```

### 爬取新浪热搜数据

```python
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
```

#### ==详细代码见spider.py文件==

### 项目代码介绍

static文件夹和template文件夹中存放项目的前端代码，主要使用了jquery和echarts技术进行前端展示。

### 如何使用该项目

**首先安装相关依赖库，详见requirements.txt**

**之后更改spider.py文件中的get_conn函数，修改为自己的数据库参数，新建cov数据库并将cov.sql导入到cov数据库中**

**cov.sql文件新建了四个表，分别为dayinfo，details，history，hotsearch**

**之后运行spider.py文件爬取数据并导入数据库，最后运行app.py启动项目。**





