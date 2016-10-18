import pandas as pd
import numpy as np
import datetime
import os
import pandas_datareader.data as wb
from lxml.html import parse





def industry_group():
    root = os.path.expanduser('~/Google Drive/OLD/Hunt/')
    stocks = pd.read_csv('/Users/duncangh/PycharmProjects/RT Outstanding/DataSets/S&P 500 Stocks.csv')

    # group by industry name -- There should be directory for each indsutry
    industry_groups = stocks.groupby('Sector')

    for ind in industry_groups.groups:
        stock_path = root + 'Stocks/' + ind + '/'
        option_path = root + 'Options/' + ind + '/'
        ind_stocks = industry_groups.get_group(ind)
        for s in list(ind_stocks['Symbol'].unique()):
            s_file = stock_path + s + '.csv'
            o_file = option_path + s + '.csv'

            # read what is in files
            try:
                s_old = pd.read_csv(s_file)
                o_old = pd.read_csv(o_file)
                s_old.append(wb.get_data_yahoo(s)).to_csv(s_file)
                o_old.append(Options(s).loop()).to_csv(o_file)
            except:
                print('failed options %s' % s)

pd.set_option('display.width', 1500)


class Options:
    def __init__(self, ticker):
        self.url = 'http://www.nasdaq.com/symbol/' + ticker + '/option-chain?dateindex='

    def loop(self):
        frames = []
        for i in range(4):
            url = self.url + str(i)
            frames.append(self._options(self._get_root(url)))
        df = pd.concat(frames)
        df['Today'] = datetime.datetime.today().strftime('%d %B %Y')
        return df

    def _get_root(self, url):
        doc = parse(url)
        root = doc.getroot()
        tables = root.findall('.//table')
        return tables[5]

    def _options(self, calls):
        header = ['Calls', 'Last', 'Chg', 'Bid', 'Ask', 'Vol', 'Open Int', 'Root', 'Strike',
                  'Puts', 'Last', 'Chg', 'Bid', 'Ask', 'Vol', 'Open Int']
        rows = calls.findall('.//tr')
        data = [unpack(r) for r in rows[1:]]
        df = pd.DataFrame(data, columns=header)
        return df

def unpack(row, kind='td'):
    elts = row.findall('.//%s'%kind)
    return [val.text_content() for val in elts]

industry_group()