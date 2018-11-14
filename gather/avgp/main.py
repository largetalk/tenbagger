from datetime import datetime
from datetime import timedelta
import pandas as pd
from collections import defaultdict
from sqlalchemy.sql import exists
from tu import getStockList
from tu import getTradeCal
from tu import getStockDaily
from db import Stock
from db import TradeCal
from db import TradeDaily
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
    def getOneYearCal(cls, exchange, year):
        key = '%s_%s' % (exchange, year)
        if year in cls.__cache__:
            return cls.__cache__[key]
        with session_scope() as session:
            one_year_cals = defaultdict(lambda:[])
            for m in range(1, 13):
                date = datetime(year, m, 1).date()
                tradeCal = session.query(TradeCal).filter_by(exchange=exchange, date=date).first()
                if tradeCal is None:
                    print("exchange %s date %s can't find trade cal" % (exchange, date))
                    continue
                for day in tradeCal.getCals():
                    one_year_cals[m].append('%s%02d%s' % (year, m, day))
            cls.__cache__[key] = one_year_cals
            return one_year_cals

def fetchAndSaveTradeDaily():
    with session_scope() as session:
        for ts_code, list_date in session.query(Stock.ts_code, Stock.list_date):
            fetchOneStockDaily(session, ts_code, list_date)

def fetchOneStockDaily(sess, ts_code, list_date):
    td = sess.query(TradeDaily).filter_by(ts_code=ts_code).order_by(TradeDaily.date.desc()).first()
    today = datetime.now().date()
    if td is not None:
        from_date = td.date
    else:
        from_date = max(datetime(2000, 1, 1).date(), list_date)
    
    exchange = 'SSE' if ts_code.endswith('.SH') else 'SZSE'
    for year in range(from_date.year, today.year + 1):
        start_date = '%s0101' % year
        if year == from_date.year:
            start_date = '%s%02d01' % (year, from_date.month)
        end_date = '%s1231' % year
        cal_dic = TradeCalCache.getOneYearCal(exchange, year)
        df = getStockDaily(ts_code, start_date, end_date)
        for m in range(1, 13):
            date = datetime(year, m, 1).date()
            closes = []
            vols = []
            amounts = []
            mflag = False
            for cal in cal_dic[m]:
                oneDF = df[df['trade_date'] == cal]
                if len(oneDF.index) < 1:
                    closes.append('-')
                    vols.append('-')
                    amounts.append('-')
                else:
                    mflag = True
                    item = oneDF.iloc[0]
                    closes.append(str(item.close))
                    vols.append(str(item.vol))
                    amounts.append(str(item.amount))
            if mflag:
                tradeDaily = sess.query(TradeDaily).filter_by(ts_code=ts_code, date=date).first()
                if tradeDaily is None:
                    tradeDaily = TradeDaily(ts_code=ts_code,
                                           date=date)
                tradeDaily.closes = TradeDaily.DATE_DELIMITER.join(closes)
                tradeDaily.vols = TradeDaily.DATE_DELIMITER.join(vols)
                tradeDaily.amounts = TradeDaily.DATE_DELIMITER.join(amounts)
                sess.add(tradeDaily)
        sess.commit()
    

if __name__ == '__main__':
    #fetchAndSaveStockList()
    #fetchAndSaveTradeCal()
    #with session_scope() as session:
    #    fetchOneStockDaily(session, '300760.SZ', datetime(2018,1,1).date())
    fetchAndSaveTradeDaily()
