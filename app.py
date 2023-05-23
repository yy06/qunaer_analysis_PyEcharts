import joblib
from flask import Flask, render_template, request, session
import json
import os
import random
import mysql

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')  # 登录页面
def login():
    return render_template('page/login.html')


@app.route('/index')  # 首页
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])  # 注册页面
def register():
    if request.method == 'GET':
        return render_template('page/register.html')
    else:
        id = request.form.get('id')
        username = request.form.get('username')
        password = request.form.get('password')
        sex = request.form.get('sex')
        age = request.form.get('age')
        sql = 'select * from user_info where username = {0}'.format(repr(username))
        res = mysql.query(sql)
        if len(res) > 0:
            return '该账号有人注册过了哦'
        sql = "insert into user_info(`username`,`userid`,`password`,`age`,`sex`) values('%s','%s','%s','%s','%s')" % (
            username, id, password, age, sex)
        mysql.insert(sql)
        return 'true'


@app.route('/user_password', methods=['GET', 'POST'])  # 修改密码
def user_password():
    return render_template('page/user_password.html')


@app.route('/userpassword', methods=['GET', 'POST'])  # 修改密码
def userpassword():
    data = request.form.get('data')
    data = json.loads(data)
    if data['new_password'] == data['new_password1']:
        sql = "select * from user_info where `id` = '" + data['userid'] + "' and `password` = '" + data[
            'old_password'] + "'"
        res = mysql.query(sql)
        if len(res) > 0:
            sql = 'UPDATE user_info SET password={0} where id = {1}'.format(repr(data["new_password"]),
                                                                            data['userid'])
            mysql.insert(sql)
            data = {
                "state": "true",
                "info": "修改成功！"
            }
            return json.dumps(data)
        else:
            data = {
                "state": "F",
                "info": "旧密码错误"
            }
            return json.dumps(data)
    else:
        data = {
            "state": "F",
            "info": "两次密码不一致"
        }
        return json.dumps(data)


@app.route('/user_login', methods=['GET', 'POST'])  # 验证登录
def user_login():
    id = request.form.get('username')
    password = request.form.get('password')
    sql = "select `id` from user_info where `userid` = '" + id + "' and `password` = '" + password + "'"
    res = mysql.query(sql)
    if len(res) > 0:
        for i in res:
            data = {
                'id': i[0],
                'state': "OK"
            }
            session['id'] = i[0]
            return json.dumps(data)
    else:
        data = {
            'state': "false_1"
        }
        return json.dumps(data)


@app.route('/yly', methods=['GET', 'POST'])  # 数据查看
def yly():
    data = []
    sql = 'select * from yanglaoyuan'
    res = mysql.query(sql)
    for i in res:
        j = list(i)
        j[7] = str(j[7]).replace('                                                                         ',
                                 ',').replace('                                                ', ',').replace(
            '                                              ', '')[1:].replace(',                    ', '')
        j[6] = str(j[6]).replace('  ', ',')
        data.append(j)
    return render_template('page/yly.html', data=data)


@app.route('/yly1', methods=['GET', 'POST'])  # 搜索结果
def yly1():
    word = request.args.get('word')
    data = []
    sql = 'select * from yanglaoyuan'
    res = mysql.query(sql)
    for i in res:
        if word in str(i):
            j = list(i)
            j[7] = str(j[7]).replace('                                                                         ',
                                     ',').replace('                                                ', ',').replace(
                '                                              ', '')[1:].replace(',                    ', '')
            j[6] = str(j[6]).replace('  ', ',')
            data.append(j)
    return render_template('page/yly.html', data=data)


@app.route('/nvyou', methods=['GET', 'POST'])  # 数据查看
def nvyou():
    data = []
    sql = 'select * from nvyou'
    res = mysql.query(sql)
    for i in res:
        j = list(i)
        data.append(j)
    return render_template('page/nvyou.html', data=data)


@app.route('/nvyou1', methods=['GET', 'POST'])  # 搜索结果
def nvyou1():
    word = request.args.get('word')
    data = []
    sql = 'select * from nvyou'
    res = mysql.query(sql)
    for i in res:
        if word in str(i):
            j = list(i)
            data.append(j)
    return render_template('page/nvyou.html', data=data)

@app.route('/mrys', methods=['GET', 'POST'])  # 数据查看
def mrys():
    data = []
    sql = 'select * from mrys'
    res = mysql.query(sql)
    for i in res:
        j = list(i)
        data.append(j)
    return render_template('page/mrys.html', data=data)


@app.route('/mrys1', methods=['GET', 'POST'])  # 搜索结果
def mrys1():
    word = request.args.get('word')
    data = []
    sql = 'select * from mrys'
    res = mysql.query(sql)
    for i in res:
        if word in str(i):
            j = list(i)
            data.append(j)
    return render_template('page/mrys.html', data=data)



@app.route('/sc_jd', methods=['GET', 'POST'])  # 收藏旅游
def sc_jd():
    data = json.loads(request.form.get('data'))
    dataid = data['id']
    userid = json.loads(request.form.get('userid'))
    sql = 'select * from sc_jd where userid={0} and dataid={1}'.format(repr(userid), repr(dataid))
    res = mysql.query(sql)
    if len(res) > 0:
        return '您已经收藏过了哦'
    else:
        sql = "insert into sc_jd(`userid`,`dataid`) values('%s','%s')" % (
            userid, dataid)
        mysql.insert(sql)
        return '收藏成功'


@app.route('/del_scjd', methods=['GET', 'POST'])  # 取消收藏
def del_scjd():
    data = json.loads(request.form.get('data'))
    dataid = data['id']
    userid = session.get('id')
    sql = 'delete from sc_jd where userid={0} and dataid={1}'.format(repr(userid), repr(dataid))
    mysql.insert(sql)
    return '删除成功'


@app.route('/my_jd')
def my_jd():
    userid = session.get('id')
    sql = 'select dataid from sc_jd where userid={0} '.format(repr(userid))
    res = mysql.query(sql)
    dataid = []
    data = []
    for i in res:
        dataid.append(i[0])
    for i in dataid:
        sql = 'select * from nvyou where id={0}'.format(repr(i))
        res = mysql.query(sql)
        for i in res:
            data.append(list(i))
    return render_template('page/sc_jd.html', data=data)


@app.route('/sc_yly', methods=['GET', 'POST'])  # 收藏养老院
def sc_yly():
    data = json.loads(request.form.get('data'))
    dataid = data['id']
    userid = json.loads(request.form.get('userid'))
    sql = 'select * from sc_yly where userid={0} and dataid={1}'.format(repr(userid), repr(dataid))
    res = mysql.query(sql)
    if len(res) > 0:
        return '您已经收藏过了哦'
    else:
        sql = "insert into sc_yly(`userid`,`dataid`) values('%s','%s')" % (
            userid, dataid)
        mysql.insert(sql)
        return '收藏成功'


@app.route('/del_scyly', methods=['GET', 'POST'])  # 取消收藏
def del_scyly():
    data = json.loads(request.form.get('data'))
    dataid = data['id']
    userid = session.get('id')
    sql = 'delete from sc_yly where userid={0} and dataid={1}'.format(repr(userid), repr(dataid))
    mysql.insert(sql)
    return '删除成功'


@app.route('/my_yly')
def my_yly():
    userid = session.get('id')
    sql = 'select dataid from sc_yly where userid={0} '.format(repr(userid))
    res = mysql.query(sql)
    dataid = []
    data = []
    for i in res:
        dataid.append(i[0])
    for i in dataid:
        sql = 'select * from yanglaoyuan where id={0}'.format(repr(i))
        res = mysql.query(sql)
        for i in res:
            j = list(i)
            j[7] = str(j[7]).replace('                                                                         ',
                                     ',').replace('                                                ', ',').replace(
                '                                              ', '')[1:].replace(',                    ', '')
            j[6] = str(j[6]).replace('  ', ',')
            data.append(j)
    return render_template('page/sc_yly.html', data=data)

@app.route('/sc_mrys', methods=['GET', 'POST'])  # 收藏旅游
def sc_mrys():
    data = json.loads(request.form.get('data'))
    dataid = data['id']
    userid = json.loads(request.form.get('userid'))
    sql = 'select * from sc_mrys where userid={0} and dataid={1}'.format(repr(userid), repr(dataid))
    res = mysql.query(sql)
    if len(res) > 0:
        return '您已经收藏过了哦'
    else:
        sql = "insert into sc_mrys(`userid`,`dataid`) values('%s','%s')" % (
            userid, dataid)
        mysql.insert(sql)
        return '收藏成功'


@app.route('/del_scmrys', methods=['GET', 'POST'])  # 取消收藏
def del_scmrys():
    data = json.loads(request.form.get('data'))
    dataid = data['id']
    userid = session.get('id')
    sql = 'delete from sc_mrys where userid={0} and dataid={1}'.format(repr(userid), repr(dataid))
    mysql.insert(sql)
    return '删除成功'


@app.route('/my_mrys')
def my_mrys():
    userid = session.get('id')
    sql = 'select dataid from sc_mrys where userid={0} '.format(repr(userid))
    res = mysql.query(sql)
    dataid = []
    data = []
    for i in res:
        dataid.append(i[0])
    for i in dataid:
        sql = 'select * from mrys where id={0}'.format(repr(i))
        res = mysql.query(sql)
        for i in res:
            data.append(list(i))
    return render_template('page/sc_mrys.html', data=data)

import echarts
echarts.page_simple_layout()
@app.route('/sjfx')
def sjfx():
    # page = echarts.page_simple_layout()
    # page.render("page/sjfx.html")
    return render_template('page/sjfx.html')


if __name__ == '__main__':
    app.run(debug=True)
