import pymysql



def coon():
    con = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='test',
                          charset='utf8')  # 连接数据库
    cur = con.cursor()
    return con, cur


def close():
    con, cur = coon()  # 关闭数据库
    cur.close()
    con.close()


def query(sql):
    con, cur = coon()  # 查询数据库
    cur.execute(sql)
    res = cur.fetchall()
    close()
    return res


def insert(sql):
    con, cur = coon()  # 删除、修改数据库表
    cur.execute(sql)
    con.commit()
    close()