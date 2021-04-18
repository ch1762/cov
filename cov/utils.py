import time
import pymysql

def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")


def get_conn():
    # 建立连接
    conn = pymysql.connect(host="localhost", user="root", password="root", db="cov", charset="utf8")
    # c创建游标A
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql,*args):
    """

    :param sql:
    :param args:
    :return:
    """
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res


def get_c1_data():
    sql = "select confirm,nowConfirm,heal,dead from history where ds=(select " \
    "ds from history order by ds desc limit 1)"
    res = query(sql)
    return res[0]

def get_c2_data():
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res

def get_l1_data():
    sql = "select ds,nowConfirm from history"
    res = query(sql)
    return res

def get_l2_data():
    sql = "select ds,confirm_add,suspect_add,heal_add,dead_add from history"
    res = query(sql)
    return res

def get_r1_data():
    sql = 'select city,zero from dayinfo where day_time = ' \
          '(select day_time from dayinfo order by day_time desc limit 1) ' \
          'order by zero desc limit 5'
    res = query(sql)
    return res

def get_r2_data():
    sql = "select content from hotsearch order by id desc limit 50"
    res = query(sql)
    return res

if __name__ == "__main__":
    print(get_c2_data())
    #print(test())