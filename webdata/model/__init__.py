from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


HOST = '39.105.43.226'
PORT = '3306'
DATABASE = 'webdata'
USERNAME = 'abc'
PASSWORD = 'mysqlpsw'
# 创建对象的基类:
Base = declarative_base()


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                       .format(USERNAME,PASSWORD,HOST,PORT,DATABASE))

#返回数据库会话
def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session