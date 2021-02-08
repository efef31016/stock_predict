import numpy as np
import requests
import pandas as pd
import datetime
from time import sleep

def transform_date(date):
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d  #民國轉西元

def transform_data(data):
    data[0] = datetime.datetime.strptime(transform_date(data[0]), '%Y/%m/%d')
    if data[7][0] == 'X':
      data[1] = 2
    elif data[7][0] == '+':
      data[1] = 1
    else:
      data[1] = 0  #把千進位的逗點去除,  +/-/X表示漲/跌/不比價

    return [data[0],data[1]]


def get_stock_history(date, stock_no):
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % ( date, stock_no)
    r = requests.get(url) #檢查狀態碼 print(r.status_code)
    data = r.json()
    data = data['data']   #該月份好幾天的九個特徵值(我們只要日期與漲跌)

    ll=[]

    for d in range(len(data)):
      ll.append(transform_data(data[d]))

    return ll #進行資料格式轉換


def create_df(date,stock_no):
    s = pd.DataFrame(get_stock_history(date, stock_no))
    s.columns = ['date','change']
    stock = []
    for i in range(len(s)):
        stock.append(stock_no)
    s['stockno'] = pd.Series(stock ,index=s.index)  #新增股票代碼欄，之後所有股票進入資料表才能知道是哪一張股票
    datelist = []
    for i in range(len(s)):
        datelist.append(s['date'][i])
    s.index = datelist  #索引值改成日期
    s2 = s.drop(['date'],axis = 1)  #刪除日期欄位
    mlist = []
    for item in s2.index:
        mlist.append(item.month)
    s2['month'] = mlist  #新增月份欄位

    return s2

st = 2010
num = 10
listDji = ['2330','2454','2317','2303','2308','1301','2412','1303','2891','2881','2882','1216','2886','3008','2002','2882','1326','2327','2885','2379','2382','2892','1101','2357','2207','2880','3045','4938','2912','2395','2474','2887','2883','6505','2890','2801','1402','4904','1101','9910','2105','2408'] #,'3034','3711','5871','5880','6515','5876','6669','2633',聯詠抓不到
df = pd.DataFrame()

for i in range(len(listDji)):
  for j in range(st, st+num):
    for k in range(1,13):
      sleep(15)
      if k < 10:
        t = j*10
        result = create_df('%s%s01'%(t,k), listDji[i])
      else:
        result = create_df('%s%s01'%(j,k), listDji[i])
      print(result)
      df = df.append(result)

  compression_opts = dict(method='zip', archive_name='%s.csv' % int(listDji[i]))
  df.to_csv('%s.zip' % int(listDji[i]), index=False, 
            compression=compression_opts)  