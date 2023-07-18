import hashlib
import threading

import pymysql

from db.db_manage import DB
from ui.loginWidget import Ui_loginForm
from PyQt5.QtWidgets import QWidget, QMessageBox
from startWin import MainWindow
from config.config import Config


class logWin(QWidget, Ui_loginForm):
    def __init__(self):
        super(logWin, self).__init__()
        self.setupUi(self)
        self.config = Config()
        self.config_ini = self.config.read_config()
        self.db = pymysql.connect(
            host="localhost",
            port=int(self.config_ini['db_set']['port']),
            user=self.config_ini['db_set']['user_name'],
            password=self.config_ini['db_set']['password'],
            charset='utf8mb4',
        )
        self.database_name = self.config_ini['db_set']['database_name']
        self.user_table=self.config_ini['db_set']['form_1']
        self.cursor = self.db.cursor()
        self.connect_db()
        self.Login.clicked.connect(self.login)
        self.Registe.clicked.connect(self.register)

    def login(self):
        if self.Account.text() == '' or self.Password.text() == '':
            QMessageBox.warning(self, "*", "输入不能为空")
        else:
            username = self.Account.text()
            password = self.Password.text()
            admit=self.check_credentials(username, password)
            if admit==1:
                QMessageBox.warning(self, "登录失败", "密码错误")
                # self.Account.clear()
                self.Password.clear()
            elif admit==2:
                # QMessageBox.information(self, "登录成功", "登录成功！")
                self.win = MainWindow()
                self.win.show()
                self.hide()
                # cursor.close()
                # db.close()
            elif admit==3:
                QMessageBox.warning(self, "登录失败", "不存在此用户")
                self.Account.clear()
                self.Password.clear()

    def register(self):

        if self.Account.text() == '' or self.Password.text() == '':
            QMessageBox.warning(self, "*", "输入不能为空")
        else:
            username = self.Account.text()
            password = self.Password.text()
            if self.check_username(username):
                QMessageBox.warning(self, "注册失败", "用户名已存在！")
                self.Account.clear()
                self.Password.clear()
            else:
                encrypted_password = self.sha256_hash(password)
                self.add_user(username, encrypted_password)

    def check_credentials(self, username, password):

        sql = f"SELECT * FROM {self.user_table};"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            if username == row[0] and self.sha256_hash(password) != row[1]:
                return 1
            elif username == row[0] and self.sha256_hash(password) == row[1]:
                return 2
        return 3

    def check_username(self, username):

        sql = f"SELECT id FROM {self.user_table}"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            if (username == row[0]):
                print("ID:", row[0])
                return True

        return False

    def add_user(self, username, password):

        data = (username, password)
        sql = f"INSERT INTO {self.user_table} (id,pass_word) VALUES (%s,%s)"
        self.cursor.execute(sql, data)
        self.db.commit()
        QMessageBox.information(self, "注册成功", "注册成功！")

    def sha256_hash(self, message):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode('utf-8'))
        return sha256_hash.hexdigest()

    def connect_db(self):
        # database_name = 'your_database'
        query = f"SHOW DATABASES LIKE '{self.database_name}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            print("数据库已存在，连接到数据库")
            self.db.close()
            self.db = pymysql.connect(
                host="localhost",
                port=int(self.config_ini['db_set']['port']),
                user=self.config_ini['db_set']['user_name'],
                password=self.config_ini['db_set']['password'],
                charset='utf8mb4',
                database=self.config_ini['db_set']['database_name']
            )
            self.cursor = self.db.cursor()
            self.creat_table()
            pass
        else:
            print("数据库不存在，创建数据库")
            sql = f"CREATE DATABASE {self.database_name}"
            self.cursor.execute(sql)
            print(f"数据库 {self.database_name} 创建成功")
            # self.db.commit()
            # self.db.close()
            self.db = pymysql.connect(
                host="localhost",
                port=int(self.config_ini['db_set']['port']),
                user=self.config_ini['db_set']['user_name'],
                password=self.config_ini['db_set']['password'],
                charset='utf8mb4',
                database=self.config_ini['db_set']['database_name']
            )
            self.cursor = self.db.cursor()
            self.creat_table()
            self.db.commit()

    def creat_table(self):
        # table = ["user", "functions"]
        table_name_1 = self.config_ini['db_set']['form_1']
        table_name_2 =self.config_ini['db_set']['form_2']
        # table=[table_name_1,table_name_2]
        query = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database_name}' AND TABLE_NAME = '{table_name_1}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            print("表已存在，连接到表")
            pass
        # 连接到表进行后续操作
        else:
            print("表不存在，创建表")
            # 创建数据库
            self.cursor.execute(f"CREATE TABLE {table_name_1} (id VARCHAR(20), pass_word VARCHAR(200), PRIMARY KEY (id))")
            # file = self.config_ini['main_project']['project_path'] + self.config_ini['db']['user']

            db=DB(" ")
            new_thread=threading.Thread(target=db.insert_table,kwargs={'choose':3})
            new_thread.start()


        query = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database_name}' AND TABLE_NAME = '{table_name_2}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            print("表已存在，连接到表")
            pass
        # 连接到表进行后续操作
        else:
            print("表不存在，创建表")
            # 创建数据库
            self.cursor.execute(f"CREATE TABLE {table_name_2} (name VARCHAR(20), level VARCHAR(20), description VARCHAR(500), PRIMARY KEY (name))")

            f = self.config_ini['main_project']['project_path'] + self.config_ini['db']['danger_funcs']
            db = DB(f)
            # print(db.get_key())
            new_thread = threading.Thread(target=db.insert_table, kwargs={'choose': 1})
            new_thread.start()
