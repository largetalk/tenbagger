from datetime import datetime
from tu import getStockList
from db import Stock
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
    

if __name__ == '__main__':
    fetchAndSaveStockList()
