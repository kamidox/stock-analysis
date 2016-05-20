# stock-analysis

股票数据分析

## 数据来源

雅虎财经网站提供股票日历史数据下载接口。

直接在浏览器地址中数据网址即可 http://table.finance.yahoo.com/table.csv?s=股票代码。上证股票是股票代码后面加上.ss，深证股票是股票代码后面加上.sz。例如查询中国石油的历史数据，直接在浏览器中输入：http://table.finance.yahoo.com/table.csv?s=601857.ss

深市数据链接：http://table.finance.yahoo.com/table.csv?s=000001.sz 上市数据链接：http://table.finance.yahoo.com/table.csv?s=600000.ss

另外，上证综指代码：000001.ss，深证成指代码：399001.SZ，沪深300代码：000300.ss

字段格式

Date Open High Low Close Volume Adj Close 分别是：日期、开盘价、最高价、最低价、收盘价、成交量、复权收盘价

获取指定时间范围的数据

【例子】 取 2012年1月1日 至 2012年4月19日的数据 http://table.finance.yahoo.com/table.csv?a=0&b=1&c=2012&d=3&e=19&f=2012&s=600000.ss

## 功能说明

程序提供了一些基础的股票数据获取和股票数据分析的方法。

### 股票列表

股票列表数据来自[东方财富网](http://quote.eastmoney.com/stocklist.html)，没有实时更新。目前数据是 2015年12月份获取出来的数据。SZ.txt 是深市股票列表，SH.txt 是沪市的全部股票列表。

### 获取股票数据

原理上，使用 yahoo 财经的 API 接口下载股票数据。具体实现的代码在 [yahoo_stock.py](https://github.com/kamidox/stock-analysis/blob/master/yahoo_stock.py)。比如，直接运行这个文件将会下载从 2015-10-1 到现在的所有中小股 (以 002 开头) 的股票数据。下载完的股票数据将放在 `yahoo-data` 目录下。

### 数据分析

数据分析开发很多模型来分析，这里使用股票的振幅来进行简单分析。一般来讲，振幅大的股票意味着风险比较高，但收益也比较高。风险与收益一定是动态平衡正相关。

振幅分析实现在 [stock_analysis.py](https://github.com/kamidox/stock-analysis/blob/master/stock_analysis.py) 里。函数 `amplitude()` 默认分析最近 30 天，所有在 `yahoo-data` 目录下的股票数据的振幅排名。

### 其他

[yahoo-stock.ipynb](https://github.com/kamidox/stock-analysis/blob/master/yahoo-stock.ipynb) 是关键函数演示场所。
