from werkzeug.security import generate_password_hash,check_password_hash
from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 't_user'
    u_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    u_name = db.Column(db.String(20),nullable=False)
    u_pwd = db.Column(db.String(20), nullable=False)
    u_tel = db.Column(db.String(20),nullable=False)
    u_addr = db.Column(db.String(100),nullable=False)
    u_img = db.Column(db.String(100))
    u_time = db.Column(db.DateTime, default=datetime.now)
        # def __init__(self,*args,**kwargs):
        #     u_tel = kwargs.get('u_tel')
        #     u_name = kwargs.get('u_name')
        #     u_pwd = kwargs.get('u_pwd')
        #
        #     self.u_tel = u_tel
        #     self.u_name = u_name
        #     self.u_pwd = generate_password_hash(u_pwd)
        #
        # def check_password(self,raw_password):
        #     result = check_password_hash(self.u_pwd,raw_password)
        #     return result

class Goods(db.Model):
    __tablename__ = 't_goods'
    g_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    g_name = db.Column(db.String(30),nullable=False)
    g_desc = db.Column(db.Text,nullable=False)
    g_class = db.Column(db.Integer,db.ForeignKey('t_class.c_id'),nullable=False)
    g_sell = db.Column(db.Integer,db.ForeignKey('t_user.u_id'),nullable=False)
    g_price = db.Column(db.Integer,nullable=False)
    g_img = db.Column(db.String(100))
    g_discount = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String(50),nullable=False)
    g_time = db.Column(db.DateTime,default=datetime.now)
    g_u_tel = db.Column(db.String(20))
    g_u_qq = db.Column(db.String(20))
    g_u_wechat = db.Column(db.String(30))

    author = db.relationship('User',backref=db.backref('goods'))

class Class(db.Model):
    __tablename__ = 't_class'
    c_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    c_name = db.Column(db.String(20),nullable=False)

class Comment(db.Model):
    __tablename__ = 't_comment'
    cm_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cm_content = db.Column(db.Text,nullable=False)
    cm_time = db.Column(db.DateTime,default=datetime.now)
    goods_id = db.Column(db.Integer,db.ForeignKey('t_goods.g_id'))
    author_id = db.Column(db.Integer,db.ForeignKey('t_user.u_id'))

    goods = db.relationship('Goods', backref=db.backref('comments'),order_by=cm_time.desc())
    author = db.relationship('User',backref=db.backref('comments'))

class Message(db.Model):
    __tablename__ = 't_message'
    m_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    m_gid = db.Column(db.Integer,nullable=False)
    m_sell = db.Column(db.Integer, nullable=False)
    m_content = db.Column(db.String(100), nullable=False)
    m_time = db.Column(db.String(30), nullable=False)


class Order(db.Model):
    __tablename__ = 't_order'
    o_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    o_gid = db.Column(db.Integer,db.ForeignKey('t_goods.g_id'))
    o_bid = db.Column(db.Integer,db.ForeignKey('t_user.u_id'))
    o_time = db.Column(db.DateTime,default=datetime.now)
    o_money = db.Column(db.Float,nullable=False)
    o_addr = db.Column(db.String(50),nullable=False)
    o_tel = db.Column(db.String(20),nullable=False)
    o_ordernumber = db.Column(db.String(50),nullable=False)
    o_desc = db.Column(db.String(100),nullable=False)
    o_postcode = db.Column(db.String(10),nullable=False)

class Attention(db.Model):
    __tablename__ = 't_attention'
    at_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    at_uid = db.Column(db.Integer,nullable=False)
    ated_gid = db.Column(db.Integer,db.ForeignKey('t_goods.g_id'))
    ated_uid = db.Column(db.Integer,db.ForeignKey('t_user.u_id'))

    ated_author = db.relationship('User',backref=db.backref('author_info'))
