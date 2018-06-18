import argparse
import calendar
import datetime
import json
import logging
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

from symbol import Symbol

#
# logger
#
logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse the command-line arguments
    :return: parsed result dict
    """
    parser = argparse.ArgumentParser(
        description='Evaluate the net value of investments')

    parser.add_argument('begin', help='Investment begin YYYYMM')
    parser.add_argument('end', help='Investment end YYYYMM')
    parser.add_argument('-amount', required=True, type=int, help='$ to invest every month')
    parser.add_argument('-symb', required=True, nargs='+', help='The symbols to invest, ex: "vt aapl"')

    args = parser.parse_args()

    try:
        args.begin = datetime.datetime.strptime(args.begin, '%Y%m').date()
        args.end = datetime.datetime.strptime(args.end, '%Y%m').date()
    except:
        logger.error('Incorrect date value, use YYYYMM, ex: 200806')
        sys.exit(1)

    if args.end < args.begin:
        logger.error('Invalid end date')
        sys.exit(1)

    return args


def main():
    args = parse_args()

    total_invest_amount = 0.0
    total_invest_amount_with_interest = 0.0
    interest_rate = 0.011
    symbol = {}
    investment = {}
    for symb in args.symb:
        investment[symb] = 0.0
        symbol[symb] = Symbol(symb)

    investment_value = {}
    investment_return = {}
    current_month = args.begin
    while current_month <= args.end:
        total_invest_amount += args.amount
        total_invest_amount_with_interest = total_invest_amount_with_interest * interest_rate / 12 + total_invest_amount_with_interest + args.amount
        month_days = calendar.monthrange(current_month.year, current_month.month)[1]

        current_investment_value = {
            'total_invest': total_invest_amount,
            'bank_saving': total_invest_amount_with_interest
        }

        for symb in args.symb:
            price = symbol[symb].get_price(
                (current_month.strftime('%Y%m') + '01', current_month.strftime('%Y%m') + str(month_days)))
            shares = float(args.amount) / price[1]
            investment[symb] = investment[symb] + shares
            current_investment_value[symb] = investment[symb] * price[3]
            investment_return[symb] = float(current_investment_value[symb] - total_invest_amount) / float(
                total_invest_amount)

        investment_value[current_month.strftime('%Y%m') + str(month_days)] = current_investment_value

        current_month += datetime.timedelta(days=month_days)

    investment_result = pd.DataFrame.from_dict(investment_value, orient='index')
    logger.info('writing investment detail to %s', os.path.join(os.path.dirname(__file__), 'output.csv'))
    investment_result.to_csv(os.path.join(os.path.dirname(__file__), 'output.csv'))
    logger.info('investment returns: \n%s', json.dumps(investment_return, indent=2))
    investment_result.plot(kind='bar')
    plt.show()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    main()
