# -*- coding: utf-8 -*-
import urllib
import os
import datetime
import pandas as pd
import numpy as np


def retrive_stock_data(stockid, folder):
    """ 下载整个股票数据 """

    end = datetime.date.today().strftime('%Y%m%d')
    url = 'http://quotes.money.163.com/service/chddata.html?' \
          'code=%s&start=19900101&end=%s' \
          '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;PCHG;TURNOVER;VOTURNOVER;VATURNOVER' \
          % (stockid, end)
    print('downloading %s to %s from %s' % (stockid, folder, url))
    fname = os.path.join(folder, '%s.csv' % stockid[-6:])
    if not os.path.isdir(folder):
        os.mkdir(folder)
    urllib.request.urlretrieve(url, fname)


def update_stock_data(stockid, folder, startdate=None):
    """ 更新股票数据，如果不存在，则下载。如果存在，则只更新最近日期的数据

    :param: stockid: stock id, like 600690.ss, must contain postfix
    :param: folder: folder name to store downloaded data
    :param: startdate: download data from start date
    """

    if not os.path.isdir(folder):
        os.mkdir(folder)

    fname = os.path.join(folder, '%s.csv' % stockid[-6:])
    if startdate is None and not os.path.exists(fname):
        retrive_stock_data(stockid, folder)
        return

    data = None
    last_date = None
    if os.path.exists(fname):
        data = pd.read_csv(fname, index_col='日期', parse_dates=True)
        last_date = data.iloc[0:1].index.tolist()[0]

    startdate = pd.Timestamp(startdate)
    if last_date and startdate < last_date:
        startdate = last_date + pd.Timedelta(days=1)
    today = pd.Timestamp(datetime.date.today())
    if today - startdate < pd.Timedelta(days=1):
        print('Nothing to update. %s last date is %s.' % (stockid, last_date))
        return

    start = startdate.date().strftime('%Y%m%d')
    end = today.date().strftime('%Y%m%d')
    url = 'http://quotes.money.163.com/service/chddata.html?' \
          'code=%s&start=%s&end=%s' \
          '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;PCHG;TURNOVER;VOTURNOVER;VATURNOVER' \
          % (stockid, start, end)
    print('updatting %s [%s - %s] form %s' % (stockid, startdate.date(), today.date(), url))
    temp_file = fname + '.tmp'
    try:
        urllib.request.urlretrieve(url, temp_file)
        update_data = pd.read_csv(temp_file, index_col='日期', parse_dates=True, encoding='gb18030')
    except Exception as e:
        print(e)
        return

    if data is None:
        data = update_data
    else:
        data = data.append(update_data)
    data.sort_index(ascending=False, inplace=True)
    data.to_csv(fname, mode='w')
    os.unlink(temp_file)


def stock_list(files, marks):
    """ 合并股票列表，输出合并后的，可以通过 api 获取的股票列表

    files: a sequence like ['SH.txt', 'SZ.txt']
    marks: a sequence map to files, like ['0', '1']
    """
    if len(files) != len(marks):
        print('error: size of files and marks not match.')
        return

    stocks = []
    for i in range(len(files)):
        data = pd.read_csv(files[i], header=None, names=['name', 'id'], dtype={'id': np.str}, skipinitialspace=True)
        data['id'] = marks[i] + data['id']
        stocks.append(data)

    data = pd.concat(stocks)
    print('%d files. %d stocks.' % (len(files), len(data)))
    return data


def update_stock_data_batch(filter=None, startdate=None):
    """ 批量更新所有股票数据 """

    slist = stock_list(['SH.txt', 'SZ.txt'], ['0', '1'])
    if filter:
        slist = slist[slist['id'].str.endswith(filter)]
    for i in range(len(slist)):
        s = slist.iloc[i]
        update_stock_data(s['id'], 'stock-data', startdate=startdate)


if __name__ == '__main__':
    update_stock_data_batch('600690', startdate='1990-01-01')

