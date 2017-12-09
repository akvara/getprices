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
# INPUT_FOLDER = '/home/andrius/Downloads/'
INPUT_FOLDER = 'quotes/'
OUTPUT_FOLDER = '/home/andrius/MEGA/OMX/'


def convert_files(input_files_array):
    lines = 0
    tickers = 0

    output_file = OUTPUT_FOLDER + OUTPUT_FILE_NAME

    with open(output_file, 'w') as csv_output:
        spam_writer = csv.writer(csv_output, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        spam_writer.writerow(HEADER)
        for input_file in input_files_array:
            ticker = os.path.splitext(os.path.basename(input_file))[0]
            print("Converting ticker {}".format(ticker))
            with open(input_file, 'r') as csv_input:
                spam_reader = csv.reader(csv_input, delimiter=',', quotechar="'")
                next(spam_reader)
                for row in spam_reader:
                    spam_writer.writerow(convert_format(row, ticker))
                    lines += 1
            tickers += 1
    return tickers, lines


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
    input_files_array = list()
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".csv"):
            input_files_array.append(INPUT_FOLDER + file)

    convert_files(input_files_array)