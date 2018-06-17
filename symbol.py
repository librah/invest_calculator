import logging
import os
import requests
import json
import datetime
import pandas as pd

#
# logger
#
logger = logging.getLogger(__name__)

cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
APIKEY = 'alphavantage_apikey'

#
# DateFrame columns
#
C_OPEN = '1. open'
C_HIGH = '2. high'
C_LOW = '3. low'
C_CLOSE = '4. close'
C_VOLUME = '5. volume'


class Symbol(object):
    def __init__(self, symb):
        self._symb = symb.lower()
        self._cache_file = os.path.join(cache_dir, symb + '.json')
        self._cache_file_mdate = None  # datetime.date instance when the file was updated
        self._data = None

    def _download_history_price(self):
        if os.getenv(APIKEY, '') == '':
            logger.error('Missing required "alphavantage_apikey" env variable')
            raise Exception('Missing required "alphavantage_apikey" env variable')

        resp = requests.get('https://www.alphavantage.co/query', {
            "function": "TIME_SERIES_DAILY",
            "symbol": self._symb,
            "apikey": os.getenv(APIKEY, ''),
            "outputsize": "full"
        })

        if resp.status_code != 200:
            logger.error('Unable to download "%s" history price from https://www.alphavantage.co\n%s', self._symb, resp.text)
            raise Exception('Unable to download history price')

        with open(self._cache_file, "w") as f:
            json.dump(resp.json, indent=2)

    def _load_price_data(self):
        if not os.path.isfile(self._cache_file):
            self._download_history_price()

        with open(self._cache_file) as f:
            raw_data = json.load(f)
            self._cache_file_mdate = datetime.date.fromtimestamp(os.path.getmtime(self._cache_file))

        df = pd.DataFrame.from_dict(raw_data['Time Series (Daily)'], orient='index', dtype='float')
        df.index = pd.to_datetime(df.index)

        self._data = df

    def _can_refresh_cache(self):
        # if the cache file was created today, no refesh needed
        return datetime.date.today() != self._cache_file_mdate

    def get_price(self, range):
        """
        :param range: a date string, ex: '20180617', or date range tuple ('20180101', '20180617').
        :return: a tuple of price (open, high, low, close) in the specified time range.
          None returned if
        """
        if self._data is None:
            self._load_price_data()

        if isinstance(range, basestring):
            if range not in self._data.index:
                return None
            else:
                row = self._data.loc[range]
                return (row[C_OPEN],
                        row[C_HIGH],
                        row[C_LOW],
                        row[C_CLOSE])
        else:
            data_range = self._data.index.date
            data_start_date = data_range[0]
            data_end_date = data_range[-1]

            d1, d2 = range
            query_start_date = datetime.datetime.strptime(d1, '%Y%m%d').date()
            query_end_date = datetime.datetime.strptime(d2, '%Y%m%d').date()
            assert query_end_date > query_start_date

            if query_start_date >= data_start_date and query_end_date <= data_end_date:
                row_in_range = self._data.loc[d1:d2]
                max_values = row_in_range.max()
                min_values = row_in_range.min()
                return (row_in_range.iloc[0][C_OPEN],
                        max_values[C_HIGH],
                        min_values[C_LOW],
                        row_in_range.iloc[-1][C_CLOSE])
            else:
                return None
