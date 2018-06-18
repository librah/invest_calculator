[![Build Status](https://travis-ci.org/librah/invest_calculator.svg?branch=master)](https://travis-ci.org/librah/invest_calculator)

Calculate the return of investment

## Download historical data
Before evaluate the investment performance, you must download the symbol's history price data
to `cache/` directory.

- For US stock/ETF, use [Alpha Vantage](https://www.alphavantage.co) API, ex:
  `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=amzn&apikey=your_key&outputsize=full`
- For Taiwan stock, use https://www.cnyes.com, ex: `https://www.cnyes.com/twstock/ps_historyprice/0050.htm`

## Usage

```sh
$ pip install -r requirements.txt
$ python evaluate.py 200801 201805 -amount 1000 -symb vt 0050
writing investment detail to output.csv
investment returns:
{
  "0050": -0.005171154313227709,
  "vt": 0.044299066648239044
}
```
