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
