import sqlite3
import requests
import re
import os
from bs4 import BeautifulSoup


class table:
    def __init__(self, primary, columns, size):
        self.primary = primary
        self.columns = columns
        self.size = size


class SqlIO:
    def __init__(self, database):
        self.database = database
        self.connect = sqlite3.connect(database)
        self.tables = {}

    def SqlTableExists(self, table_name):
        sql = "select name from main.sqlite_master where type = \'table\'"
        cursor = self.connect.cursor()
        count = cursor.execute(sql)
        for row in count:
            if row[0] == table_name:
                cursor.close()
                return True
        cursor.close()
        return False

    def SqlMake(self, table_name, primary, primary_len, terms, terms_len):
        sql = "create table " + table_name + " (" + primary + " varchar(" + str(primary_len) + ") "
        for i in terms:
            sql += ", " + i + " varchar(" + str(terms_len) + ") "
        sql += ")"
        self.tables[table_name] = (table(primary, terms, len(terms) + 1))
        cursor = self.connect.cursor()
        cursor.execute(sql)
        cursor.close()

    def SqlReader(self, table_name, column):
        sql = "select " + column + " from " + table_name
        cursor = self.connect.cursor()
        tmp = []
        for row in cursor.execute(sql):
            tmp.append(row[0])
        cursor.close()
        return tmp

    def SqlInsert(self, table_name, data):
        # insert a record in dictionary form, throw exception when primary key is invalid
        sql = "insert into " + table_name + " values " + "("
        current_table = self.tables[table_name]
        for i in current_table.size:
            sql += ",?"
        sql += ")"
        tmp = []
        if current_table.primary in data:
            tmp.append(data[current_table.primary])
        else:
            raise RuntimeError("null primary key")
        for i in current_table.columns:
            if i in data:
                tmp.append(data[i])
            else:
                tmp.append('null')
        cursor = self.connect.cursor()
        cursor.execute(sql, tuple(tmp))
        cursor.close()

    def __del__(self):
        self.connect.commit()
        self.connect.close()


class Parser:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
        self.Seieexsb = 'http://bjwb.seiee.sjtu.edu.cn/bkjwb'
        self.Electsys = 'http://electsys.sjtu.edu.cn/edu/'
        self.Seieexsbdb = 'seieexsb'
        self.Electsysdb = 'electsys'

    def SeieeParser(self, url):
        data = []
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')
        rurl = r'/bkjwb/info[\w/.]+'
        for term in soup.find_all('a', href=re.compile(rurl)):
            data.append('http://bjwb.seiee.sjtu.edu.cn' + term['href'])
        return data

    def ElectParser(self, url):
        data = []
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'lxml')
        for term in soup.find_all('a', class_='news'):
            data.append(term['href'])
        return data


def main():
    db = "sjtu.db"
    sqlobj = SqlIO(db)
    reg = re.compile(r'.*如何看待.*')
    check = []
    count = 0
    for i in sqlobj.SqlReader('QA', 'question'):
        if reg.search(i) is not None:
            if reg.search(i).string not in check:
                count +=1
                check.append(reg.search(i).string)
                print(reg.search(i).string)
    print(count)

if __name__ == '__main__':
    main()
