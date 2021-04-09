import configparser
import pymysql


class MyDButil():
    conn = None
    def __init__(self):
        super(MyDButil, self).__init__()
        config = configparser.ConfigParser()
        config.read("Util/config.ini", encoding="utf-8")
        config.sections()  # 获取section节点
        config.options('mysql')  # 获取指定section 的options即该节点的所有键
        self.__db_name = config.get('mysql', "db.name")
        self.__db_host = config.get('mysql', "db.host")
        self.__db_port = config.getint('mysql', "db.port")
        self.__db_user = config.get('mysql', "db.user")
        self.__db_password = config.get('mysql', "db.password")
        self.conn = self.connect()
        if self.conn:
            self.cursor = self.conn.cursor()

    def getName(self):
        return self.__db_name

    def getHost(self):
        return self.__db_host

    def getPort(self):
        return self.__db_port

    def getUser(self):
        return self.__db_user

    def getPassword(self):
        return self.__db_password

    def find(self):
        return 0

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.__db_host, port=self.__db_port, user=self.__db_user,
                                        password=self.__db_password, db=self.__db_name, charset='utf8')
        except Exception as data:
            self._logger.error("连接数据库失败, %s" % data)
            self.conn = None
        return self.conn

    def fetch_all(self, sql):
        res = ''
        if (self.conn):
            try:
                self.cursor.execute(sql)
                res = self.cursor.fetchall()
            except Exception as data:
                res = False
                self._logger.warn("查询结果失败, %s" % data)
        return res

    def update(self, sql):
        flag = False
        if (self.conn):
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                flag = True
            except Exception as data:
                flag = False
                self._logger.warn("更新数据库失败, %s" % data)
        return flag

# db=DButil()
# connect=db.connect()
# cur=connect.cursor()
# sql="select * from test"
# cur.execute(sql)
# result=cur.fetchall()
# print(result)

# db=MyDButil()
# sql="select * from 模板1"
# print(db.fetch_all(sql))

# sql="create table 模板5(label_id varchar(144),origin_data varchar(122),detect_data varchar(122),result varchar(122)) CHARSET=utf8"
# print(db.update(sql))

# sql="drop table if exists 模板6;
# create table 模板6(label_id varchar(255) not null,origin_data varchar(255),detect_data varchar(255),result varchar(255));"
# db=MyDButil()
# sql="show tables from ocr;"
# flag=db.fetch_all(sql)
# for item in flag:
#     print(item[0])
