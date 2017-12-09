import time
import datetime
import requests

time_from = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple()))
time_till = int(time.mktime(datetime.datetime.today().timetuple()))

url = 'https://query1.finance.yahoo.com/v7/finance/download/VRX?period1={}&period2={}&interval=1d&events=history&crumb=Tf9jj9gtri5'.format(time_from, time_till)
# url = 'https://finance.yahoo.com/quote/MORL/history?period1=1483221600&period2=1512770400&interval=1d&filter=history&frequency=1d'

session = requests.Session()
print(session.cookies.get_dict())

r = requests.get(url)
print(r.json())
print(r.headers)

session = requests.Session()
print(session.cookies.get_dict())

# print(r.content)

def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    # Note: possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    crumb2 = crumb.decode('unicode-escape')
    return cookie, crumb2