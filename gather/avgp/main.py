from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
from collections import defaultdict
from sqlalchemy.sql import exists
from sqlalchemy import or_, and_
from sqlalchemy import not_
from tu import getStockList
from tu import getTradeCal
from tu import getStockDaily
from tu import getDailyBasic
from tu import getOneDailyBasic
from db import Stock
from db import TradeCal
from db import TradeDaily
from db import DailyStats
from db import session_scope


def fetchAndSaveStockList():
    data = getStockList()
    with session_scope() as session:
        for i in data.index:
            item = data.iloc[i]
            stock = session.query(Stock.ts_code).filter_by(ts_code=item['ts_code']).first()
            if stock is not None and stock.list_status == 'L':
                continue
            if stock is not None:
                stock.list_status = 'L'
            else:
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
            print('add stock %s' % item['name'].encode('utf-8'))

def updateStockListStatus():
    data = getStockList(list_status='D')
    with session_scope() as session:
        for i in data.index:
            item = data.iloc[i]
            stock = session.query(Stock.ts_code).filter_by(ts_code=item['ts_code']).first()
            if stock is None or stock.list_status == 'D':
                continue
            stock.list_status = 'D'
            session.add(stock)
            print('update stock %s list_status to D' % item['name'].encode('utf-8'))



def fetchAndSaveTradeCal():
    #exchange = 'SZSE'
    exchange = 'SSE'
    years = range(2017, 2020)
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
                print("add traceCal %s" % date)


class TradeCalCache():
    __cache__ = {}

    @classmethod
    def getOneYearCal(cls, exchange, year):
        key = '%s_%s' % (exchange, year)
        if key in cls.__cache__:
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
            fetchOneDailyBasic(session, ts_code, list_date)

def needFetchDaily(td, cal_dic):
    if td is None:
        return True
    today = datetime.now().date()
    yc = datetime(today.year, today.month, 1).date()
    if td.date < yc:
        return True

    cals = [ int(x[-2:]) for x in cal_dic[today.month] ]
    if datetime.now().hour > 15:
        cals = filter(lambda x: x <= today.day, cals)
    else:
        cals = filter(lambda x: x < today.day, cals)

    closes = td.closes.split(TradeDaily.DATE_DELIMITER)
    #print cals
    #print closes
    if closes[len(cals) - 1] != '-':
        return False
    return True
    

def fetchOneStockDaily(sess, ts_code, list_date):
    td = sess.query(TradeDaily).filter(TradeDaily.ts_code==ts_code, TradeDaily.closes!=None).order_by(TradeDaily.date.desc()).first()
    today = datetime.now().date()
    if td is not None:
        #if td.year == today.year and td.month == today.month: #temporarily for performace
        #    return
        from_date = td.date
    else:
        from_date = max(datetime(2000, 1, 1).date(), list_date)
    
    exchange = 'SSE' if ts_code.endswith('.SH') else 'SZSE'
    for year in range(from_date.year, today.year + 1):
        cal_dic = TradeCalCache.getOneYearCal(exchange, year)
        if not needFetchDaily(td, cal_dic):
            #print('skip fetch %s stock daily' % ts_code)
            continue

        start_date = '%s0101' % year
        if year == from_date.year:
            start_date = '%s%02d01' % (year, from_date.month)
        end_date = '%s1231' % year
        if year == today.year:
            end_date = '%s%02d31' % (year, today.month)
        print("fetch %s stock daily from %s to %s" % (ts_code, start_date, end_date))
        df = getStockDaily(ts_code, start_date, end_date)
        for m in range(1, 13):
            date = datetime(year, m, 1).date()
            if date > today:
                break
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

def fetchOneDailyBasic(sess, ts_code, list_date):
    td = sess.query(TradeDaily).filter(TradeDaily.ts_code==ts_code, TradeDaily.pb!=None).order_by(TradeDaily.date.desc()).first()
    today = datetime.now().date()
    if td is not None:
        #if td.year == today.year and td.month == today.month: #temporarily for performace
        #    return
        from_date = td.date
    else:
        from_date = max(datetime(2000, 1, 1).date(), list_date)
    
    exchange = 'SSE' if ts_code.endswith('.SH') else 'SZSE'
    for year in range(from_date.year, today.year + 1):
        cal_dic = TradeCalCache.getOneYearCal(exchange, year)
        if not needFetchDaily(td, cal_dic):
            #print('skip fetch %s stock daily' % ts_code)
            continue

        start_date = '%s0101' % year
        if year == from_date.year:
            start_date = '%s%02d01' % (year, from_date.month)
        end_date = '%s1231' % year
        if year == today.year:
            end_date = '%s%02d31' % (year, today.month)
        print("fetch %s daily basic from %s to %s" % (ts_code, start_date, end_date))
        df = getDailyBasic(ts_code, start_date, end_date)
        for m in range(1, 13):
            date = datetime(year, m, 1).date()
            if date > today:
                break
            pettm = []
            pb = []
            totalmv = []
            mflag = False
            for cal in cal_dic[m]:
                oneDF = df[df['trade_date'] == cal]
                if len(oneDF.index) < 1:
                    pettm.append('-')
                    pb.append('-')
                    totalmv.append('-')
                else:
                    mflag = True
                    item = oneDF.iloc[0]
                    if item.pe_ttm is None or np.isnan(item.pe_ttm):
                        pettm.append('-')
                    else:
                        pettm.append('%.2f' % item.pe_ttm)
                    pb.append('%.2f' % item.pb if item.pb is not None else '-')
                    totalmv.append(str(int(item.total_mv)))
            if mflag:
                tradeDaily = sess.query(TradeDaily).filter_by(ts_code=ts_code, date=date).first()
                if tradeDaily is None:
                    tradeDaily = TradeDaily(ts_code=ts_code,
                                           date=date)
                tradeDaily.pettm = TradeDaily.DATE_DELIMITER.join(pettm)
                tradeDaily.pb = TradeDaily.DATE_DELIMITER.join(pb)
                tradeDaily.totalmv = TradeDaily.DATE_DELIMITER.join(totalmv)
                sess.add(tradeDaily)
        sess.commit()


def calc_median_mean():
    with session_scope() as session:
        ds = session.query(DailyStats).order_by(DailyStats.date.desc()).first()
        if ds is not None:
            from_date = ds.date
        else:
            from_date = datetime(2000, 1, 1).date()
        today = datetime.now().date()
        for year in range(from_date.year, today.year + 1):
            m_f = 1
            m_t = 13
            if from_date.year == today.year:
                m_f = from_date.month
                m_to = today.month + 1
            for m in range(m_f, m_t):
                d = datetime(year, m, 1).date()
                if d > today:
                    print("calc median done")
                    return
                tradeCal = session.query(TradeCal).filter_by(date=d).first()
                if tradeCal is None:
                    print("trade cal %s not found" % d)
                    continue
                month_closes = []
                month_pettm = []
                month_pb = []
                for tradeDaily in session.query(TradeDaily).filter_by(date=d):
                    prices = [ float(x) if x != '-' else np.nan for x in tradeDaily.closes.split(',') ]
                    month_closes.append(prices)
                    if tradeDaily.pettm is not None and len(tradeDaily.pettm) > 0:
                        pettm = [ float(x) if x != '-' else np.nan for x in tradeDaily.pettm.split(',') ]
                        month_pettm.append(pettm)
                    if tradeDaily.pb is not None:
                        pb = [ float(x) if x != '-' else np.nan for x in tradeDaily.pb.split(',') ]
                        month_pb.append(pb)
                if len(month_closes) < 1 or len(month_pettm) < 1:
                    print('trade daily %s not found' % d)
                    continue
                df  = pd.DataFrame(np.array(month_closes), columns=tradeCal.getCals())
                median = df.median()
                df_pettm  = pd.DataFrame(np.array(month_pettm), columns=tradeCal.getCals())
                mean_pettm = df_pettm.mean()
                df_pb  = pd.DataFrame(np.array(month_pb), columns=tradeCal.getCals())
                mean_pb = df_pb.mean()
                for col in tradeCal.getCals():
                    close_d = datetime(year, m, int(col)).date()
                    #if np.isnan(median[col]) or median[col] < 0.01:
                    #    print('median %s is unexists' % close_d)
                    #    continue
                    ds = session.query(DailyStats).filter_by(date=close_d).first()
                    if ds is None:
                        ds = DailyStats(date=close_d)
                    if not np.isnan(median[col]) and median[col] > 0.1:
                        ds.median_close = median[col]
                    if not np.isnan(mean_pettm[col]) and mean_pettm[col] > 1:
                        ds.mean_pettm = mean_pettm[col]
                    if not np.isnan(mean_pb[col]) and mean_pb[col] > 0.1:
                        ds.mean_pb = mean_pb[col]
                    session.add(ds)
                session.commit()


def plot_median_close(start_date=None):
    import matplotlib.pyplot as plt
    lst = []
    with session_scope() as session:
        if start_date is not None:
            dss = session.query(DailyStats).filter(DailyStats.date > start_date).order_by(DailyStats.date).all()
        else:
            dss = session.query(DailyStats).order_by(DailyStats.date).all()
        for ds in dss:
            lst.append([ds.date, ds.median_close])
        df = pd.DataFrame(np.array(lst), columns=['date', 'close'])

    df.plot(x = 'date', y = 'close', kind="line", title="median close", grid=True)
    plt.show()

def main():
    today = datetime.now()
    if today.day == 1:
        fetchAndSaveStockList()
        fetchAndSaveTradeCal()
        updateStockListStatus()
    fetchAndSaveTradeDaily()
    calc_median_mean()
    plot_median_close()

if __name__ == '__main__':
    main()
    #with session_scope() as session:
    #    fetchOneStockDaily(session, '300139.SZ', datetime(2018,1,1).date())
    #    fetchOneDailyBasic(session, '300139.SZ', datetime(2018,1,1).date())

