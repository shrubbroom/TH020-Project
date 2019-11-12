import sqlite3
import requests
import re
import os
from bs4 import BeautifulSoup


class SqlIO:
    def __init__(self, database):
        self.database = database
        self.connect = sqlite3.connect(database)

    def  SqlMake(self,table):
        pass

    def SqlReader(self, table):
        sql = 'if object_id(\'' + table + '\') is not null'
        cursor = self.connect.cursor
        if cursor.execute(sql):
            pass
        # todo



class Parser:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
        self.Seieexsb = 'http://bjwb.seiee.sjtu.edu.cn/bkjwb'
        self.Seieexsbdb = 'seieexsb'

    def SeieeParser(self, url):
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')
        rurl = r'/bkjwb/info[\w/.]+'
        for term in soup.find_all('a', href=re.compile(rurl)):
            print(term.text)
            print('http://bjwb.seiee.sjtu.edu.cn' + term['href'])

    def seiee(self):
        self.SeieeParser(self.Seieexsb)


def main():
    p = Parser()
    p.seiee()


if __name__ == '__main__':
    main()
