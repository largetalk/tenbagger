#coding:utf8
import tushare as ts
print(ts.__version__)

from settings import tushare_token
ts.set_token(tushare_token)
pro = ts.pro_api()
#pro = ts.pro_api(tushare_token)

def getStockList(list_status=None):
    '''
    input:
        is_hs   str N   是否沪深港通标的，N否 H沪股通 S深股通
        list_status str N   上市状态： L上市 D退市 P暂停上市
        exchange    str N   交易所 SSE上交所 SZSE深交所 HKEX港交所

    output fields:
        ts_code str TS代码
        symbol  str 股票代码
        name    str 股票名称
        area    str 所在地域
        industry    str 所属行业
        fullname    str 股票全称
        enname  str 英文全称
        market  str 市场类型 （主板/中小板/创业板）
        exchange    str 交易所代码
        curr_type   str 交易货币
        list_status str 上市状态： L上市 D退市 P暂停上市
        list_date   str 上市日期
        delist_date str 退市日期
        is_hs   str 是否沪深港通标的，N否 H沪股通 S深股通
    '''
    #data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    #return pro.stock_basic(exchange='', list_status='L')
    if list_status is not None:
        return pro.stock_basic(list_status=list_status)
    return pro.stock_basic()

def getStockDaily(ts_code, start_date, end_date):
    '''
    input:
        ts_code str N   股票代码（二选一）
        trade_date  str N   交易日期（二选一）
        start_date  str N   开始日期(YYYYMMDD)
        end_date    str N   结束日期(YYYYMMDD)

    output:
        ts_code str 股票代码
        trade_date  str 交易日期
        open    float   开盘价
        high    float   最高价
        low float   最低价
        close   float   收盘价
        pre_close   float   昨收价
        change  float   涨跌额
        pct_change  float   涨跌幅
        vol float   成交量 （手）
        amount  float   成交额 （千元）
    '''
    try:
        return pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date, fields="ts_code,trade_date,close,vol,amount") #get one stock daily history
    except BaseException, e:
        print type(e), e.message
        raise e
    #or
    #df = pro.daily(trade_date='20180810') # get all stock one day data

def getOneDaily(trade_date):
    return pro.daily(trade_date=trade_date, fields="ts_code,trade_date,close,vol")

def getDailyBasic(ts_code, start_date, end_date):
    '''
    input:
        ts_code str N   股票代码（二选一）
        trade_date  str N   交易日期（二选一）
        start_date  str N   开始日期(YYYYMMDD)
        end_date    str N   结束日期(YYYYMMDD)

    output:
        ts_code str 股票代码
        trade_date  str 交易日期
        close   float   当日收盘价
        turnover_rate   float   换手率（%）
        turnover_rate_f float   换手率（自由流通股）
        volume_ratio    float   量比
        pe  float   市盈率（总市值/净利润）
        pe_ttm  float   市盈率（TTM）
        pb  float   市净率（总市值/净资产）
        ps  float   市销率
        ps_ttm  float   市销率（TTM）
        total_share float   总股本 （万股）
        float_share float   流通股本 （万股）
        free_share  float   自由流通股本 （万）
        total_mv    float   总市值 （万元）
        circ_mv float   流通市值（万元）
    '''
    try:
        return pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields="ts_code,trade_date,pe_ttm,pb,total_mv") #get one stock daily history
    except BaseException, e:
        print type(e), e.message
        raise e
    #or
    #df = pro.daily(trade_date='20180810') # get all stock one day data

def getOneDailyBasic(trade_date):
    return pro.daily_basic(trade_date=trade_date, fields="ts_code,trade_date,pe_ttm,pb,total_mv")

def getTradeCal(year, exchange=''):
    '''
    input:
        exchange    str N   交易所 SSE上交所 SZSE深交所
        start_date  str N   开始日期
        end_date    str N   结束日期
        is_open int N   是否交易 0休市 1交易
    output:
        exchange    str 交易所 SSE上交所 SZSE深交所
        cal_date    str 日历日期
        is_open int 是否交易 0休市 1交易
        pretrade_date   str 上一个交易日
    '''
    start_date = '%s0101' % year
    end_date = '%s1231' % year
    df = pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
    return df[df['is_open'] == 1]
