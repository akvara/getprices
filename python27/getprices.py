#!/usr/bin/python -tt

import sys, urllib, re, time, datetime

TABLE_COL1 = r'<tr><td class="yfnc_tabledata1" nowrap align="right">(\w\w\w)\s(\d+),\s(\d\d\d\d)</td>'
TABLE_COL2 = r'<td class="yfnc_tabledata1" align="right">([\d,]+\.\d\d)</td>'
TABLE_COL3 = TABLE_COL2
TABLE_COL4 = TABLE_COL2
TABLE_COL5 = TABLE_COL2
TABLE_COL6 = r'<td class="yfnc_tabledata1" align="right">([\d,]+)</td>'
TABLE_COL7 = TABLE_COL2 + '</tr>'

HEADER = '<TICKER>,<PER>,<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>'

YAHOO_URL = 'http://finance.yahoo.com/q/hp?s=GLD+Historical+Prices'
#YAHOO_URL = 'http://finance.yahoo.com/q/hp?s=GLD&d=3&e=13&f=2013&g=d&a=10&b=18&c=2004&z=66&y=66'
GOOGLE_URL = 'https://www.google.com/finance?q='
OMX_URL = 'http://kurmis.org/csv/OMX.prn'
DJI_URL = 'http://kurmis.org/csv/DJI.prn'
OMX_daily_URL = 'http://www.nasdaqomxbaltic.com/market/?pg=mainlist&lang=en&downloadcsv=1&csv_style=english'
kurmis_URL = 'http://kurmis.org/grafikai/csv_omx.php'
FaTa_URL = 'http://www.fatalyse.com/fatalyse/ftadownload.php?lid=183'

INTPUT_FILE_NAME = 'MyStocks.lst'
OUTPUT_FILE_NAME = 'OMX.prn'


def main():

  current_url = YAHOO_URL
  current_output_file_name = 'OMX.prn'
  if len(sys.argv) >= 2:
    TICKER = sys.argv[1]
    current_url = re.sub('GLD',TICKER,current_url)
  print 'Getting "%s" into "%s"...' % (current_url,current_output_file_name)
  if len(sys.argv) >= 3:
    current_output_file_name = sys.argv[2]
  ts1 = time.time()

  prices_csv = parse_yahoo_text(wget(current_url))
  save_file(prices_csv, current_output_file_name, 'new')
  ts2 = time.time()
  print 'Done in %.4f seconds' % (ts2-ts1)


## ===== get_from ===== ##
def get_from(source, append_type):
  ts1 = time.time()
  if source=='GLD':
    save_file(parse_yahoo_text(wget(YAHOO_URL)), OUTPUT_FILE_NAME, append_type)
  elif source=='OMX':
    save_url_to_file(OMX_URL, OUTPUT_FILE_NAME, append_type)
  elif source=='DJI':
    save_url_to_file(DJI_URL, OUTPUT_FILE_NAME, append_type)
  elif source=='kurmis':
    save_url_to_file(kurmis_URL, OUTPUT_FILE_NAME, append_type)
  elif source=='google_list':
    parse_list_to_file('google',INTPUT_FILE_NAME, OUTPUT_FILE_NAME, append_type)
  elif source=='yahoo_list':
    parse_list_to_file('yahoo',INTPUT_FILE_NAME, OUTPUT_FILE_NAME, append_type)
  elif source=='OMX_daily':
    parse_OMX(OUTPUT_FILE_NAME, append_type)
  elif source=='FaTa':
    save_url_to_file(FaTa_URL, OUTPUT_FILE_NAME, append_type)
  else:
    print 'wtf?'
  ts2 = time.time()
  print "Source '%s' parsed in %.2f seconds" % (source,ts2-ts1)


## ===== wget ===== ##
## returns url's source text ##
def wget(url):
  try:
    ufile = urllib.urlopen(url)  ## get file-like object for url
    info = ufile.info()   ## meta-info about the url content
    if info.gettype() in ('text/html', 'text/plain'):
      ## print '------------------>'+'base url:' + ufile.geturl()
      text = ufile.read()  ## read all its text
      return text
  except IOError:
    print 'problem reading url:', url

## ===== parse_list_to_file ===== ##
## saves input list, parsed, to output file ##
def parse_list_to_file(source,input_filename, output_filename, append_type):
  if append_type=='append':
    text = ''
  else:
    text = HEADER+'\r\n'
  my_stock_list = [i.strip().split() for i in open(input_filename).readlines()]
  if my_stock_list[0]:
    f = open(output_filename, append_letter(append_type))
    for (counter, ticker) in enumerate(my_stock_list[0]):
      if source=='yahoo':
        ticker = re.sub('\.','-',ticker)
        current_url = re.sub('GLD',ticker,YAHOO_URL)
        print str(counter) + ': ' + ticker + ' (' + current_url +')'
        new_text = parse_yahoo_text(wget(current_url))
      elif source=='google':
        current_url = GOOGLE_URL+ticker
        print str(counter) + ': ' + ticker + ' (' + current_url +')'
        new_text = parse_google_ticker(ticker)
      if new_text and len(new_text) > 0:
        text += new_text
      else:
        print '--- ' + ticker + ' not found!'
    f.write(text)
    f.close()

## ===== save_url_to_file ===== ##
## saves url' source text to file  ##
def save_url_to_file(url, filename, append_type):
  text = wget(url)
  if text:
    if append_type=='append':
      text = text.replace(HEADER+'\r\n', '')
    f = open(filename, append_letter(append_type))
    f.write(text)
    f.close()

## ===== get_file ===== ##
def get_file(filename):
  f = open(filename, 'r')
  text = f.read()
  f.close()
  return text

## ===== save_file ===== ##
def save_file(text, filename, append_type):
  if append_type=='new' and text:
    text = HEADER + "\n" + text
  f = open(filename, append_letter(append_type))
  if text:
    f.write(text)
  f.close()

## ===== append_letter ===== ##
def append_letter(append_type):
  if append_type=='append':
    return 'a'
  else:
    return 'w'


## ===== parse_en_month ===== ##
def parse_en_month(month):
 return {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
    }.get(month, 0)

## ===== parse_yahoo_text ===== ##
def parse_yahoo_text(text):
  title = re.search(r'<title>([-^A-Z]+) Historical Prices', text)
  if title:
    output_text = ''
    tuples = re.findall(TABLE_COL1+TABLE_COL2+TABLE_COL3+TABLE_COL4+TABLE_COL5+TABLE_COL6, text)
    for one_tuple in tuples:
        ticker = title.group(1).replace('-','.').replace('^','')
        line = ticker + ',D,' + one_tuple[2] + parse_en_month(one_tuple[0]) + one_tuple[1].zfill(2) + ',0' ## Ticker, Period, Date and Time
        for i in range(len(one_tuple)):
          if i>2:
              line = line +','+re.sub(',','',one_tuple[i])
        output_text = output_text + line + ',0\n'
    return output_text

## ===== parse_google_ticker ===== ##
def parse_google_ticker(ticker):
  #text = get_file('google.txt')
  text = wget(GOOGLE_URL+ticker)

  output_text = ''
  #title = re.search(r'<div class=appbar-snippet-secondary><span>\(NYSE:(\w+)\)</span></div>', text).group(1)
  first_test = re.search(r'<meta itemprop="price"\n        content="(\d+.\d+)"', text)
  if first_test:
    current_price = first_test.group(1)
    high_low = re.search(r'<td class="key"\n          data-snapfield="range">Range\n</td>\n<td class="val">(\d+.\d+) - (\d+.\d+)', text)
    if high_low:
		low_price = high_low.group(1)
		high_price = high_low.group(2)
		open_price = re.search(r'<td class="key"\n          data-snapfield="open">Open\n</td>\n<td class="val">(\d+.\d+)', text).group(1)
		volume_groups = re.search(r'<td class="key"\n          data-snapfield="vol_and_avg">.*\n</td>\n<td class="val">(([0-9]{1,3}\,?)+.\d+)(M?)', text)
		volume_val = float(volume_groups.group(1).replace(',',''))
		if volume_groups.group(len(volume_groups.groups())) =='M':
		  volume_val = volume_val * 1000000
		data_date = re.search(r'<span class=nwp>\n(\w+)\s(\d+)', text)
		if data_date:
		  month =  parse_en_month(data_date.group(1))
		  day = data_date.group(2)
		else:
		  month = str(datetime.datetime.now().month).zfill(2)
		  day = str(datetime.datetime.now().day).zfill(2)
		ticker = ticker.replace('-','.')
		output_text += ticker + ','                    # <TICKER>
		output_text += 'D,'                            # <PER>
		output_text += str(datetime.datetime.now().year) + month + day + ',' # <DTYYYYMMDD>
		output_text += '0,'                            # <TIME>
		output_text += open_price + ','                # <OPEN>
		output_text += high_price + ','                # <HIGH>
		output_text += low_price + ','                 # <LOW>
		output_text += current_price + ','             # <CLOSE>
		output_text += str(volume_val) + ','           # <VOL>
		output_text += '0\n'                           # <OPENINT>

  return output_text

## ===== parse_google_ticker ===== ##
def parse_OMX(filename, append_type):
  import urllib2
  import string
  import codecs
  if append_type=='append':
    output_text = ''
  else:
    output_text = '' #HEADER+'\r\n'

  output_text = output_text.encode('UTF-8')
  f = urllib2.urlopen(OMX_daily_URL)
  for line in f.readlines()[1:]:

    Ticker,Name,ISIN,Currency,MarketPlace,segmentas,AveragePrice,OpenPrice,HighPrice,LowPrice,LastclosePrice,LastPrice,PriceChange,Bestbid,Bestask,Trades,Volume,Turnover  = string.split(line, '\t')
    output_text += str(Ticker)

  f.close()
  print output_text
  save_file(output_text, filename, append_type)


    # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()


  #import codecs
  #f = codecs.open('baltic_equity_list_20130326_1830.csv', "r", "utf-16" )
  #text = f.read()

  #for line in text.split('\n')[1:]:
    #elements = line.split('\t')
    # print elements[0] # Ticker
    #print elements[0] + ',' + elements[7] + ',' + elements[8] + ',' +  elements[9] + ',' + elements[11] + ','  + elements[16]

  #print parse_google_ticker('MU')

  #pattern_strings = re.compile(r"\n")
  #text = wget(OMX_URL)
  #f = open('omx.orig', 'r')

  #text = get_file('omx.orig')
  #text = str(urllib.urlopen(OMX_URL).read(), encoding='utf8')
  #ufile = urllib.urlopen(OMX_URL)  ## get file-like object for url
  #info = ufile.info()   ## meta-info about the url content
  #print info
  #text = ufile.readline()
  #print text[2:].decode('utf-16').split(',')
