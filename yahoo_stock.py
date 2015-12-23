# -*- coding: utf-8 -*-
import urllib
import os
import datetime
import pandas as pd
import numpy as np


def retrive_stock_data(stockid, folder):
    """ 下载整个股票数据 """

    url = 'http://table.finance.yahoo.com/table.csv?s=%s' % (stockid)
    print('downloading %s to %s from %s' % (stockid, folder, url))
    fname = os.path.join(folder, '%s.csv' % stockid.split('.')[0])
    if not os.path.isdir(folder):
        os.mkdir(folder)
    urllib.urlretrieve(url, fname)


def update_stock_data(stockid, folder, startdate=None):
    """ 更新股票数据，如果不存在，则下载。如果存在，则只更新最近日期的数据

    :param: stockid: stock id, like 600690.ss, must contain postfix
    :param: folder: folder name to store downloaded data
    :param: startdate: download data from start date
    """

    fname = os.path.join(folder, '%s.csv' % stockid.split('.')[0])
    if startdate is None and not os.path.exists(fname):
        retrive_stock_data(stockid, folder)
        return

    data = None
    last_date = None
    if os.path.exists(fname):
        data = pd.read_csv(fname, index_col='Date', parse_dates=True)
        last_date = data.iloc[0:1].index.tolist()[0]

    startdate = pd.Timestamp(startdate)
    if last_date and startdate < last_date:
        startdate = last_date
    today = pd.Timestamp(datetime.date.today())
    if today - startdate < pd.Timedelta(days=2):
        print('Nothing to update. %s last date is %s.' % (stockid, last_date))
        return

    print('updatting %s to from %s to %s' % (stockid, startdate.date(), today.date()))
    query = [
        ('a', startdate.month - 1),
        ('b', startdate.day),
        ('c', startdate.year),
        ('d', today.month - 1),
        ('e', today.day),
        ('f', today.year),
        ('s', stockid),
    ]
    url = 'http://table.finance.yahoo.com/table.csv?%s' % urllib.urlencode(query)
    temp_file = fname + '.tmp'
    try:
        urllib.urlretrieve(url, temp_file)
        update_data = pd.read_csv(temp_file, index_col='Date', parse_dates=True)
    except Exception, e:
        print('ERROR: error to parse %s' % stockid)
        print(e)
        return

    if data is None:
        data = update_data
    else:
        data = data.append(update_data)
    data.sort_index(ascending=False, inplace=True)
    data.to_csv(fname, mode='w')
    os.unlink(temp_file)


def stock_list(files, postfixs):
    """ 合并股票列表，输出合并后的，可以通过 yahoo api 获取的股票列表

    files: a sequence like ['SH.txt', 'SZ.txt']
    postfixs: a sequence map to files, like ['.ss', '.sz']
    """
    if len(files) != len(postfixs):
        print('error: size of files and postfixs not match.')
        return

    stocks = []
    for i in range(len(files)):
        data = pd.read_csv(files[i], header=None, names=['name', 'id'], dtype={'id': np.string0}, skipinitialspace=True)
        data['id'] += postfixs[i]
        stocks.append(data)

    data = pd.concat(stocks)
    print('%d files. %d stocks.' % (len(files), len(data)))
    return data


def update_stock_data_batch(filter=None, startdate=None):
    """ 批量更新所有股票数据 """

    slist = stock_list(['SH.txt', 'SZ.txt'], ['.ss', '.sz'])
    if filter:
        slist = slist[slist['id'].str.startswith(filter)]
    for i in range(len(slist)):
        s = slist.iloc[i]
        update_stock_data(s['id'], 'yahoo-data', startdate=startdate)

if __name__ == '__main__':
    update_stock_data_batch('002', startdate='2015-10-1')

