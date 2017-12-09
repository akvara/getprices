#!/usr/bin/python
import sys, getopt
from getprices import get_from
from datetime import datetime

def main(argv):

  try:
    opts, args = getopt.getopt(argv,"hrdv",["ryte","diena","vakare"])
  except getopt.GetoptError:
    print 'test.py -i <inputfile> -o <outputfile>'
    sys.exit(2)
  if not opts:
    print 'Usage: getbunch.py -[rdv]'
    sys.exit()

  for opt, arg in opts:
    if opt in ("-r", "--ryte"):
      get_from('GLD', 'new')
      get_from('OMX', 'append')
      get_from('kurmis', 'append')
      get_from('yahoo_list', 'append')
    elif opt in ("-d", "--diena"):
      get_from('kurmis', 'new')
    elif opt in ("-v", "--vakare"):
      get_from('google_list', 'new')
    else:
      print 'Usage: getbunch.py -[hrdv]'

  print datetime.now().strftime('%H:%M')
  raw_input('Hit Enter to close window.')

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main(sys.argv[1:])
