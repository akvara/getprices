import csv

INPUT_FILE = '/home/andrius/MEGA/OMX/CSV.csv'

C_TICKER_NAME = 0
C_DATE = 1
C_CLOSE = 5


def update_dict(data, ticker, key, value):
    cell_value = data[ticker] if ticker in data else dict()
    cell_value.update({key: value})
    data.update({ticker: cell_value})


def calc_change(first, last):
    return round((float(last) - float(first)) / float(first) * 100, 1)


if __name__ == '__main__':
    data = dict()
    row_no = 0
    first = None
    last = None
    with open(INPUT_FILE) as csvfile:
        spam_reader = csv.reader(csvfile)
        for row in spam_reader:
            # print(row)
            if row_no != 0:
                ticker = row[C_TICKER_NAME]
                price = row[C_CLOSE]
                if ticker not in data:
                    update_dict(data, ticker, 'first', price)
                update_dict(data, ticker, 'last', price)
                if not first:
                    first = row[C_DATE]
                last = row[C_DATE]
            row_no += 1

    for key in data:
        update_dict(data, key, 'change', calc_change(data[key]['first'], data[key]['last']))

    print("Data from {} to {}".format(first, last))

    for key, value in sorted((value['change'], key) for (key, value) in data.items()):
        print(value, key, '%')
