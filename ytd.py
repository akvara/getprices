import csv

# INPUT_FILE = '/home/andrius/MEGA/OMX/CSV.csv'
INPUT_FILE = '/home/andrius/MEGA/OMX/stat.csv'
YEAR_START_FILE = '/home/andrius/MEGA/OMX/20180101.csv'

C_TICKER_NAME = 0
C_DATE = 1
C_CLOSE = 5


def update_dict(data, ticker, key, value):
    # print("update_dict", ticker, key, value)
    cell_value = data[ticker] if ticker in data else dict()
    cell_value.update({key: value})
    data.update({ticker: cell_value})


def calc_change(data_cell):
    if not data_cell.get('first'):
        return 0
    if not data_cell.get('last'):
        return 0

    first = data_cell['first']
    last = data_cell['last']
    return round((float(last) - float(first)) / float(first) * 100, 1)


def get_last_price(data, spam_reader, which):
    row_no = 0
    last = None
    for row in spam_reader:
        # print(row)
        if row_no != 0:
            ticker = row[C_TICKER_NAME]
            price = row[C_CLOSE]
            # print("ticker, price", ticker, price)
            update_dict(data, ticker, which, price)
            last = row[C_DATE]
        row_no += 1
    return data, last


if __name__ == '__main__':
    data = dict()
    first = None
    last = None
    with open(YEAR_START_FILE) as csvfile:
        data, first = get_last_price(data, csv.reader(csvfile), 'first')
    with open(INPUT_FILE) as csvfile:
        data, last = get_last_price(data, csv.reader(csvfile), 'last')

    # print(first, last)
    # exit()
    for key in data:
        update_dict(data, key, 'change', calc_change(data[key]))
    print(data)

    print("Data from {} to {}".format(20180102, last))

    for key, value in sorted((value['change'], key) for (key, value) in data.items()):
        print(value, key, '%')
