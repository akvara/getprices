import ast
import csv
import datetime
import re
import sys
import time
from requests.exceptions import ConnectionError, RequestException, ReadTimeout
import requests

import settings

HEADER = ['<TICKER>', '<DTYYYYMMDD>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']
DATE = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
VOLUME = 6

OUTPUT_FILE_NAME = 'CSV.csv'
OUTPUT_FOLDER = '/home/andrius/MEGA/OMX/'
# OUTPUT_FOLDER = '~/Documents/MEGA/OMX/'

QUERY_URL = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}"


def put_data(tickers, output_folder):
    output_file = output_folder + OUTPUT_FILE_NAME
    lines = 0
    count_tickers = 0

    with open(output_file, 'w') as csv_output:
        spam_writer = csv.writer(csv_output, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        spam_writer.writerow(HEADER)
        for ticker in tickers:
            normalized_ticker = strip_country(ticker)
            sys.stdout.write("Getting {} ...".format(normalized_ticker))
            last = None
            try:
                quotes = get_quotes(ticker)
                for row in quotes:
                    converted = convert_format(row.split(','), normalized_ticker)
                    if converted:
                        last = converted[DATE + 1][4:]
                        spam_writer.writerow(converted)
                    lines += 1
                sys.stdout.write(last if last else '----')
                sys.stdout.write('\n')
                count_tickers += 1
            except (KeyError, TypeError) as error:
                sys.stdout.write("Ticker {} not found: {}.\n".format(normalized_ticker, error))
    sys.stdout.write(
        'Date {}, {} tickers, {} lines, file {}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                          count_tickers, lines, output_file))


def strip_country(ticker):
    pos = ticker.find('.')
    if pos == -1:
        return ticker
    return ticker[:pos]


# ----- Crumb utilities -----
def split_crumb_store(v):
    if not v:
        return None
    return v.split(':')[2].strip('"')


def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    if not lines:
        return None
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")


def get_cookie_value(r):
    return {'B': r.cookies['B']}


def get_page_data(symbol):
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    try:
        r = requests.get(url, timeout=10)
    except ConnectionError:
        return None, None
    except RequestException:
        return None, None
    cookie = get_cookie_value(r)

    # Code to replace possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    lines = r.content.decode('unicode-escape').strip().replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb


# ----- Quotes utilities -----
def get_quotes(symbol):
    start_date = int(time.mktime((datetime.datetime.now() + datetime.timedelta(-settings.HISTORY_DAYS)).timetuple()))
    end_date = int(time.time())
    cookie, crumb = get_cookie_crumb(symbol)
    return get_data(symbol, start_date, end_date, cookie, crumb)


def get_data(symbol, start_date, end_date, cookie, crumb):
    if not cookie:
        return None
    url = QUERY_URL.format(symbol, start_date, end_date, crumb)
    try:
        response = requests.get(url, cookies=cookie, timeout=10)
    except (ConnectionError, ReadTimeout):
        return None
    data = [s.strip() for s in response.text.splitlines()]
    return data[1:]


# ----- Format converter -----
def convert_format(csv_arr_row, ticker):
    if len(csv_arr_row) < 1 or csv_arr_row[HIGH] == 'null' or ast.literal_eval(csv_arr_row[HIGH]) == 0:
        return None
    out = list()
    out.append(ticker)
    out.append(csv_arr_row[DATE].replace('-', ''))
    out.append(csv_arr_row[OPEN])
    out.append(csv_arr_row[HIGH])
    out.append(csv_arr_row[LOW])
    out.append(csv_arr_row[CLOSE])
    out.append(csv_arr_row[VOLUME])
    return out


if __name__ == '__main__':
    output_folder = OUTPUT_FOLDER
    if len(sys.argv) > 1:
        output_folder = sys.argv[1]
    put_data(settings.TICKERS, output_folder)
