import sys
import csv
import os

HEADER = ['<TICKER>', '<DTYYYYMMDD>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']
DATE = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
VOLUME = 6

OUTPUT_FILE_NAME = 'CSV.csv'
INPUT_FOLDER = '/home/andrius/Downloads/'
OUTPUT_FOLDER = '/home/andrius/MEGA/OMX/'


def main(input_file, ticker, output_file='CSV.CSV'):
    lines = 0
    with open(input_file, 'r') as csv_input, open(output_file, 'w') as csv_output:
        spamreader = csv.reader(csv_input, delimiter=',', quotechar="'")
        next(spamreader)
        spamwriter = csv.writer(csv_output, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(HEADER)
        for row in spamreader:
            spamwriter.writerow(convert_format(row, ticker))
            lines += 1
    return lines


def convert_format(csv_arr_row, ticker):
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
    if len(sys.argv) < 2:
        print("Usage: {} ticker".format(sys.argv[0]))
        sys.exit(-1)

    input_file_name = INPUT_FOLDER + sys.argv[1] + '.csv'

    if not os.path.exists(input_file_name):
        print("File {} does not exist".format(sys.argv[1]))
        sys.exit(-1)

    base = os.path.basename(input_file_name)
    ticker = os.path.splitext(base)[0]
    output_file = OUTPUT_FOLDER + OUTPUT_FILE_NAME
    lines = main(input_file_name, ticker, output_file)

    print("Exported {} rows to {}".format(lines, output_file))
