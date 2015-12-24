# -*- coding: utf-8 -*-
import os
import pandas as pd
import datetime


def amplitude(datadir='yahoo-data', interval=30, end_date=None):
    """
    Calculate the amplitude for all stock in data dir. Return a sorted pandas.DataFrame.

    :param datadir: folder name to read stock data from
    :param interval: amplitude in this interval
    :param end_date: default to None, means that it will calculate amplitude from (now - interval) to now
    :return: A sorted pandas.DataFrame
    """

    if not os.path.isdir(datadir) or not os.path.exists(datadir):
        print('error: idirectory not exist. %s' % datadir)
        return

    if end_date is None:
        end_date = pd.Timestamp(datetime.datetime.now())

    def _ripple(fname, start, end):
        data = pd.read_csv(os.path.join(datadir, fname), index_col='Date', parse_dates=True)
        # data in file is sorted in **Descend**
        data = data.loc[end:start]

        def _ripple_radio(d):
            return d.High.max() / d.Low.min()

        if data.Low.idxmin() < data.High.idxmax():
            ripple_radio = _ripple_radio(data)
        else:
            ripple_radio = - _ripple_radio(data)
        return ripple_radio

    files = os.listdir(datadir)

    def _stock_id(fname):
        return fname.split('.')[0]

    end_date = pd.Timestamp(end_date)
    start_date = end_date - pd.Timedelta(days=interval)
    ripples_list = [(_stock_id(f), _ripple(f, start_date, end_date)) for f in files if f.endswith('.csv')]
    ripples = pd.DataFrame(ripples_list, columns=['id', 'amp'])

    all_ripples = ripples.sort_values('amp', ascending=False)

    print('head 5 recent amplitude in period of %d for all stocks in %s till %s:' % (interval, datadir, end_date))
    print(all_ripples.head(5))
    print('tail 5 recent ripples in period of %d for all stocks in %s till %s:' % (interval, datadir, end_date))
    print(all_ripples.tail(5))

    return all_ripples


if __name__ == '__main__':
    amplitude()
