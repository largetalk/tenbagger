#coding:utf8
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import Sequence
from sqlalchemy import Float
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import sessionmaker

from settings import db_url


engine = create_engine(db_url, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, Sequence('stock_id_seq'), primary_key=True)
    ts_code = Column(String(16), unique=True)
    symbol = Column(String(16))
    name = Column(String(32))
    area = Column(String(50))
    industry = Column(String(100))
    fullname = Column(String(200))
    enname = Column(String(200))
    market = Column(String(32))
    exchange = Column(String(16))
    curr_type = Column(String(16))
    list_status = Column(String(4))
    list_date = Column(Date)
    delist_date = Column(Date)
    is_hs = Column(String(4))

    def __repr__(self):
       return "<Stock(%s, %s)>" % (self.symbol, self.name)

class TradeCal(Base):
    __tablename__ = 'trade_cal'
    DATE_DELIMITER = ","

    id = Column(Integer, Sequence('tradeCal_id_seq'), primary_key=True)
    exchange = Column(String(16), nullable=False)
    date = Column(Date, nullable=False)
    cals = Column(String(100))

    __table_args__ = (
        UniqueConstraint('exchange', 'date', name='exchange_date_idx'),
    )

    def getCals(self):
        return self.cals.split(self.DATE_DELIMITER)

class TradeDaily(Base):
    __tablename__ = 'trade_daily'
    DATE_DELIMITER = ","

    id = Column(Integer, Sequence('tradeDaily_id_seq'), primary_key=True)
    ts_code = Column(String(16), nullable=False)
    date = Column(Date, nullable=False)
    closes = Column(String(256))
    vols = Column(String(360))
    amounts = Column(String(400))

    __table_args__ = (
        UniqueConstraint('ts_code', 'date', name='ts_code_date_idx'),
    )

class DailyStats(Base):
    __tablename__ = 'daily_stats'

    date = Column(Date, primary_key=True)
    median_close = Column(Float(precision=4), nullable=False)


def init_db():
    Base.metadata.create_all(engine)

#顶固删除数据库函数
def drop_db():
    Base.metadata.drop_all(engine)

#init_db()

def test():
    session = Session()
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    session.add(ed_user) #insert
    our_user = session.query(User).filter_by(name='ed').first() #select
    session.add_all([
        User(name='wendy', fullname='Wendy Williams', password='foobar'),
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='blah')]) # insert a lot
    
    ed_user.password = 'f8s7ccs'
    session.dirty #IdentitySet([<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>])
    session.new  #IdentitySet([<User(name='wendy', fullname='Wendy Williams', password='foobar')>,...
    session.commit() # commit
    session.rollback() # rollback
