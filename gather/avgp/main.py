from datetime import datetime
import pandas as pd
from collections import defaultdict
from sqlalchemy.sql import exists
from tu import getStockList
from tu import getTradeCal
from tu import getStockDaily
from db import Stock
from db import TradeCal
from db import session_scope


def fetchAndSaveStockList():
    data = getStockList()
    with session_scope() as session:
        for i in data.index:
            item = data.iloc[i]
            date = datetime.strptime(item['list_date'], '%Y%m%d').date()
            stock = Stock(ts_code=item['ts_code'],
                         symbol=item['symbol'],
                         name = item['name'].encode('utf-8'),
                         area = item['area'].encode('utf-8'),
                         industry = item['industry'].encode('utf-8'),
                         market = item['market'],
                         list_status='L',
                         list_date=date)
            session.add(stock)


def fetchAndSaveTradeCal():
    exchange = 'SZSE'
    years = range(2000, 2019)
    for y in years:
        df = getTradeCal(y, exchange=exchange)
        df  = df.cal_date.apply(lambda x: pd.Series([x[:6], x[6:]], index=['month', 'day']))
        cal_dic = defaultdict(lambda: [])
        for i in df.index:
            item = df.loc[i]
            cal_dic[item.month].append(item.day)
        with session_scope() as session:
            for k, v in cal_dic.items():
                if len(v) < 1:
                    continue
                calstr = TradeCal.DATE_DELIMITER.join(v)
                date = datetime.strptime(k, '%Y%m').date()
                #stmt = exists().where(TradeCal.exchange==exchange, TradeCal.date==date)
                tradeCal = session.query(TradeCal).filter_by(exchange=exchange, date=date).first()
                if tradeCal is None:
                    tradeCal = TradeCal(exchange=exchange,
                                        date = date,
                                        cals = calstr)
                else:
                    tradeCal.cals = calstr
                session.add(tradeCal)


class TradeCalCache():
    __cache__ = {}

    @classmethod
    def getOneYearCal(cls, year):
        if year in cls.__cache__:
            return cls.__cache__[year]
        with session_scope() as session:
            pass

def fetchAndSaveTradeDaily():
    with session_scope() as session:
        for ts_code, list_date in session.query(Stock.ts_code, Stock.list_date):
            fetchOneStockDaily(session, ts_code, list_date)

def fetchOneStockDaily(sess, ts_code, list_date):
    from_date = max(datetime(2000, 1, 1), list_date)
    today = datetime.now().date()
    for year in range(from_date.year, today.year + 1):
        start_date = '%s0101' % year
        end_date = '%s1231' % year
    

    

if __name__ == '__main__':
    #fetchAndSaveStockList()
    #fetchAndSaveTradeCal()
    pass
