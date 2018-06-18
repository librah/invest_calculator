import datetime
import json
import logging
import os

import pandas as pd

#
# logger
#
logger = logging.getLogger(__name__)

cache_dir = os.path.join(os.path.dirname(__file__), 'cache')

#
# DateFrame columns
#
C_OPEN = 'open'
C_HIGH = 'high'
C_LOW = 'low'
C_CLOSE = 'close'
C_VOLUME = 'volume'


class Symbol(object):
    def __init__(self, symb):
        self._symb = symb.lower()
        self._data = None
        for filename in (symb + '.json', symb + '.csv'):
            filename = os.path.join(cache_dir, filename)
            if os.path.isfile(filename):
                self._load_history_data(filename)
                break
        if self._data is None:
            logging.error('No symbol json/csv file found in %s for "%s"', cache_dir, symb)
            raise Exception('No symbol json/csv file found')

    def _load_history_data(self, data_file):
        file_ext = os.path.splitext(data_file)[1]
        if file_ext == '.json':
            with open(data_file) as f:
                raw_data = json.load(f)
            df = pd.DataFrame.from_dict(raw_data['Time Series (Daily)'], orient='index', dtype='float')
            df = df.rename(index=str, columns={'1. open': 'open',
                                               '2. high': 'high',
                                               '3. low': 'low',
                                               '4. close': 'close',
                                               '5. volume': 'volume'})
            df.index = pd.to_datetime(df.index)
            df = df.sort_index(0)
            self._data = df
        elif file_ext == '.csv':
            df = pd.read_csv(data_file, delim_whitespace=True, index_col=0, parse_dates=True)
            df = df.rename(index=str, columns={'Open': 'open',
                                               'High': 'high',
                                               'Low': 'low',
                                               'Close': 'close',
                                               'Volume': 'volume'})
            df.index = pd.to_datetime(df.index)
            df = df.sort_index(0)
            self._data = df

    def get_price(self, d_range):
        """
        :param d_range: a date string, ex: '20180617', or date range tuple ('20180101', '20180617').
        :return: a tuple of price (open, high, low, close) in the specified time range.
          None returned if
        """
        if isinstance(d_range, basestring):
            if d_range not in self._data.index:
                return None
            else:
                row = self._data.loc[d_range]
                if isinstance(row, pd.DataFrame):
                    row = row.iloc[0]
                return (row[C_OPEN],
                        row[C_HIGH],
                        row[C_LOW],
                        row[C_CLOSE])
        else:
            data_date = self._data.index.date
            data_start_date = data_date[0]
            data_end_date = data_date[-1]
            if data_start_date > data_end_date:
                data_start_date, data_end_date = data_end_date, data_start_date

            d1, d2 = d_range
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
