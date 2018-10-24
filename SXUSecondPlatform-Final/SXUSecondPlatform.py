from flask import Flask,render_template,request,redirect,url_for,session,g,flash
from datetime import datetime
from werkzeug.utils import secure_filename
import config
import uuid
import os
from exts import db
from decorator import login_required
from  models import User,Class,Goods,Comment,Message,Order,Attention
import Exceptions
from file_check import allowed_file
from PIL import Image
from Util import DBUtil
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    # get_goods = Goods.query.order_by(Goods.g_time.desc()).limit(3)
    sql = 'select * from t_goods ORDER BY g_time DESC limit 3'
    goodss = db.session.execute(sql)
    good_list = []
    for item in goodss:
        goods = Goods(g_id=item[0],g_sell=item[1],g_name=item[2],g_desc=item[3],g_price=item[4],g_img=item[5])
        good_list.append(goods)
    return render_template('index.html',goods_list=good_list)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        userByTel = User.query.filter(User.u_tel ==telephone,User.u_pwd == password).first()
        userByName = User.query.filter(User.u_name == telephone, User.u_pwd == password).first()
        #把用户信息保存在cookie里面
        if userByName:
            session['user_id'] = userByName.u_id
            session.permanent = True #30填内保存
            return redirect(url_for('index'))
        elif userByTel:
            session['user_id'] = userByTel.u_id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        #手机号码验证
        user = User.query.filter(User.u_tel == telephone).first()
        if not telephone or not username or not password1 or not address:
            return redirect(url_for('regist'))
        if user:
            return redirect(url_for('regist'))
        else:
           try:
               user = User(u_tel = telephone, u_name = username, u_pwd=password1,u_addr=address)
               db.session.add(user)
               db.session.commit()
               return redirect(url_for('login'))
           except Exceptions.RegisterException as msg:
               db.session.rollback()
               return redirect(url_for('regist'))


@app.route('/self_center/')
@login_required
def self_center():
    return render_template('self_center.html')

#所有上下文及模板都有的信息（这里把用户信息加入）
@app.context_processor
def my_contex_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.u_id==user_id).first()
        return {'user':user}
    return {}

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.u_id == user_id).first()
        if user:
            g.user = user

@app.route('/logout/')
@login_required
def logout():
    #session.pop('user_id')
    #del session['user_id']
    session.clear()
    return redirect(url_for('login'))

@app.route('/upload/<u_id>', methods=['GET', 'POST'])
@login_required
def upload(u_id):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            newName = str(g.user.u_id) + '_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.' + \
                      file.filename.split('.')[-1]
            user = User.query.filter(User.u_id == u_id).first()
            user.u_img = url_for('static',filename='%s/%s' % ('userImage',newName))
            db.session.commit()
            im = Image.open(file)
            im.save(os.path.join(app.static_folder, 'userImage', newName), quality=10)
    else:
        print('上传失败')
    return redirect(url_for('self_center'))


@app.route('/post_goods/',methods=['POST','GET'])
@login_required
def post_goods():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            newName = str(g.user.u_id) + '_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.' + \
                      file.filename.split('.')[-1]
            im = Image.open(file)
            im.save(os.path.join(app.static_folder, 'goodsImage', newName), quality=10)
            newGoods = Goods(g_name=request.form.get('name'),
                                     g_desc=request.form.get('description'),
                                     g_price=request.form.get('price'),
                                     g_discount=request.form.get('discount'),
                                     location=request.form.get('location'),
                                     g_class=request.form.get('type'),
                                     g_img=url_for('static',filename='%s/%s' % ('goodsImage', newName)),
                                     g_sell=g.user.u_id,
                                     g_u_qq = request.form.get('qqnum'),
                                    g_u_wechat = request.form.get('wechatnum'),
                                    g_u_tel = request.form.get('telephone')
                                     )
            db.session.add(newGoods)
            db.session.commit()
            flash(u'发布成功!')
            return redirect(url_for('index'))
            #return redirect(url_for('item', id=1))
        else:
            flash(u'似乎没有选择图片上传哦')
    return render_template('post_goods.html')

@app.route('/detail/<goods_id>/',methods=['POST','GET'])
@login_required
def detail(goods_id):
    cur_goods = Goods.query.filter(Goods.g_id == goods_id).first()
    u_id = cur_goods.g_sell
    author_name = User.query.filter(User.u_id == u_id).first().u_name
    return render_template('detail.html', goods=cur_goods, author_name=author_name)

@app.route('/book/')
def book():
    books = Goods.query.filter(Goods.g_class==1).order_by(Goods.g_time.desc()).all()
    # for book in books:
    #     print(book.g_id)
    if not books:
        print("没有二手图书信息")
    return render_template('book.html',books=books)

@app.route('/sports/')
def sports():
    sports = Goods.query.filter(Goods.g_class == 4).order_by(Goods.g_time.desc()).all()
    return render_template('sports.html',sports = sports)
@app.route('/daily_use/')
def daily_use():
    daily_uses = Goods.query.filter(Goods.g_class == 3).order_by(Goods.g_time.desc()).all()
    return render_template('daily_use.html',daily_uses = daily_uses)

@app.route('/digital/')
def digital():
    digitals = Goods.query.filter(Goods.g_class == 2).order_by(Goods.g_time.desc()).all()
    if not digitals:
        print("没有电子产品发布信息")
    return render_template('digital.html',digitals = digitals)

@app.route('/add_comment/',methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('content')
    goods_id = request.form.get('goods_id')
    goods = Goods.query.filter(Goods.g_id == goods_id).first()
    u_id = session.get('user_id')
    # comment =Comment(content=content,goods_id=goods_id,author_id=u_id)
    user = User.query.filter(User.u_id == u_id).first() #这里一定要用first
    comment = Comment(cm_content=content, goods=goods, author=user,author_id=u_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail',goods_id=goods_id))

@app.route('/my_goods/')
@login_required
def my_goods():
    goods_list = Goods.query.filter(Goods.g_sell == g.user.u_id).order_by(Goods.g_time.desc()).all()
    return render_template('my_goods.html',goods_list=goods_list)

@app.route('/search/')
def search():
        q = request.args.get('q')
        # goods_list = Goods.query.filter(Goods.g_desc.contains(q), Goods.g_name.contains(q)).all()
        print(q)
        sql = "select * from t_goods where g_desc like '%s%s%s' OR g_name LIKE '%s%s%s' order by g_time desc" % ("%",q,"%","%",q,"%")
        goodss = db.session.execute(sql)
        goods_list = []
        for item in goodss:
            print(item)
            goods = Goods(g_id=item[0], g_sell=item[1], g_name=item[2], g_desc=item[3], g_price=item[4], g_img=item[5])
            goods_list.append(goods)
        return render_template('search_result.html',goods_list = goods_list)

@app.route('/delete_goods/<goods_id>')
@login_required
def delete_goods(goods_id):
    goods = Goods.query.filter(Goods.g_id == goods_id).first()
    db.session.delete(goods)
    db.session.commit()
    goods_list = Goods.query.filter(Goods.g_sell == g.user.u_id).order_by(Goods.g_time.desc()).all()
    return render_template('my_goods.html',goods_list=goods_list)

@app.route('/modify_self_info/',methods=['POST','GET'])
@login_required
def modify_self_info():
    if request.method == 'GET':
        return render_template('modify_self_info.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        # 手机号码验证
        user = User.query.filter(User.u_tel == telephone).first()

        if password1 != password2:
            return '两次密码不相等，请核对后再填写'
        else:
            try:
                # user = User(u_tel=telephone, u_name=username, u_pwd=password1, u_addr=address)
                user.u_tel = telephone
                user.u_name = username
                user.u_pwd = password1
                user.u_addr = address
                db.session.commit()
                return redirect(url_for('login'))
            except Exceptions.RegisterException as msg:
                db.session.rollback()
                print('修改信息失败')
                return redirect(url_for('modify_self_info'))

@app.route('/modify_goods_info/<goods_id>/',methods=['POST','GET'])
@login_required
def modify_goods_info(goods_id):
    if request.method == 'GET':
        goods = Goods.query.filter(Goods.g_id == goods_id).first()
        return render_template('modify_goods_info.html',goods = goods)
    else:
        goods = Goods.query.filter(Goods.g_id == goods_id).first()
        goods.g_name = request.form.get('name')
        goods.g_desc = request.form.get('description')
        goods.g_price = request.form.get('price'),
        goods.g_discount = request.form.get('discount'),
        goods.location = request.form.get('location'),
        goods.g_class = request.form.get('type'),
        # goods.g_img = url_for('static', filename='%s/%s' % ('goodsImage', newName)),
        goods.g_sell = g.user.u_id,
        goods.g_u_qq = request.form.get('qqnum'),
        goods.g_u_wechat = request.form.get('wechatnum'),
        goods.g_u_tel = request.form.get('telephone')
        file = request.files['file']
        if file:
            # os.remove(os.getcwd()+goods.g_img)
            os.remove(os.path.join(os.getcwd(),goods.g_img))
            newName = str(g.user.u_id) + '_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.' + \
                      file.filename.split('.')[-1]
            im = Image.open(file)
            im.save(os.path.join(app.static_folder, 'goodsImage', newName), quality=10)
            goods.g_img = url_for('static', filename='%s/%s' % ('goodsImage', newName))
        db.session.commit()
        return render_template('detail.html',goods = goods)
@app.route('/my_message/<u_id>')
@login_required
def my_message(u_id):
    messages = Message.query.filter(Message.m_sell == u_id).order_by(Message.m_time.desc()).all()
    return render_template('my_message.html',messages=messages)

@app.route('/order/<goods_id>',methods=['POST','GET'])
@login_required
def order(goods_id):
    if request.method =='GET':
        goods = Goods.query.filter(Goods.g_id == goods_id).first()
        address = request.form.get('address')
        ordernumber = uuid.uuid1()
        time = datetime.now()
        telephone = request.form.get('telephone')
        order = Order(o_addr=address,o_gid=goods_id,o_bid=g.user.u_id,o_tel=telephone,o_money=goods.g_price
                      ,o_ordernumber=ordernumber,o_time=time,o_desc=goods.g_desc)
        return render_template('order.html',order=order)
    else:
        return redirect(url_for('pay',goods_id=goods_id))
@app.route('/pay/<goods_id>',methods=['POST'])
@login_required
def pay(goods_id):
    goods = Goods.query.filter(Goods.g_id == goods_id).first()
    address = request.form.get('address')
    # postcode = request.form.get('postcode')
    ordernumber = request.form.get('ordernumber')
    telephone = request.form.get('telephone')
    time = request.form.get('time')
    order = Order(o_addr=address, o_gid=goods_id, o_bid=g.user.u_id, o_tel=telephone, o_money=goods.g_price
                  , o_ordernumber=ordernumber,o_desc=goods.g_desc)
    db.session.add(order)
    db.session.commit()
    return render_template('pay.html')

@app.route('/pay_attention/<goods_id>')
@login_required
def pay_attention(goods_id):
    goods = Goods.query.filter(Goods.g_id == goods_id).first()
    is_at = Attention.query.filter(Attention.ated_gid == goods.g_id and Attention.at_uid == g.user.u_id).first()
    if is_at:
        return '你已经关注了此商品，不需要再次关注哦'
    ated_author = User.query.filter(User.u_id == goods.g_sell).first()
    attention = Attention(ated_uid=goods.g_sell,at_uid=g.user.u_id,ated_gid=goods_id,ated_author=ated_author)
    db.session.add(attention)
    db.session.commit()
    return redirect(url_for('detail',goods_id=goods_id))

@app.route('/my_attention/')
@login_required
def my_attention():
    my_attention = Attention.query.filter(Attention.at_uid == g.user.u_id).all()
    return render_template('my_attention.html',attention_list = my_attention)

@app.route('/ated_goods/<u_id>')
@login_required
def ated_post(u_id):
    goods_list = Goods.query.filter(Goods.g_sell == u_id).order_by(Goods.g_time.desc()).all()
    return render_template('ated_post.html', goods_list=goods_list)

@app.route('/success/')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    # app.run(host='127.0.0.1',port=9999)
    app.run(host='127.0.0.1',port=5000)