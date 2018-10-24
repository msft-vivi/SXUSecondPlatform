import mysql.connector
from mysql.connector import errorcode

class DBUtil(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='945151065.',host ='39.105.89.107',database='second_platform')
        self.cursor = self.conn.cursor()
    # 注册 用的插入
    def insert(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit() #conn提交事务
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
            self.conn.rollback()
        finally:
            self.cursor.close()

    def select(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
        finally:
            self.cursor.close()
    def update(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
            self.conn.rollback()
        finally:
            self.cursor.close()
    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
            #异常时候回滚
            self.conn.rollback()
        finally:
            self.cursor.close()

if __name__ == '__main__':
    db = DBUtil()

    #向用户表中插入 注册信息
    insert_user_sql = "INSERT INTO t_user(u_name,u_pwd,u_tel,u_addr) VALUES ('%s','%s','%s','%s')" %(
        'lihua','123','15855376093','山西大同');
    db.insert(insert_user_sql)

    #查询用户信息
    select_user_sql = "SELECT * FROM t_goods WHERE g_class = 1"
    #result = db.select(select_user_sql)
    #print(result)

    #更新二手商品信息
    #update_goods_sql = "UPDATE t_goods SET g_price = 20 WHERE g_id = 2"
    #db.update(update_goods_sql)


    # #删除二手商品
    # delete_goods_sql = "DELETE FROM t_goods WHERE g_id = 2"
    # db.delete(delete_goods_sql)


