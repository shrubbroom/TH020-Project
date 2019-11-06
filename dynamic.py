import os
import re
from time import sleep
from selenium import webdriver, common
from bs4 import BeautifulSoup
import codecs
import sqlite3
import requests
from selenium.common.exceptions import TimeoutException
import time
from pympler import tracker, summary, muppy
from selenium.webdriver.firefox import options
from selenium.webdriver.support.wait import WebDriverWait


class QAItem:
    question_url = ''
    question = ''
    question_description = ''
    answerer = ''
    answer_url = ''
    answer = ''

    def load(self):
        cursor = conn.cursor()
        sql = "insert into QA values (?, ? ,?, ?,? ,?)"
        para = (
            self.question_url, self.question, self.question_description, self.answerer, self.answer_url, self.answer)
        cursor.execute(sql, para)
        cursor.close()


class WebConnector:
    def __init__(self):
        self.path = "D:\\geckodriver"
        self.option = webdriver.FirefoxOptions()
        self.option.add_argument("-headless")
        self.option.set_preference('permissions.default.image', 2)
        self.driver = webdriver.Firefox(self.path, options=self.option)
        self.count = 0

    def reload(self):
        self.driver.quit()
        print('reconnecting...')
        self.driver = webdriver.Firefox(self.path, options=self.option)

    def scroll_wait(self, time, freq, height):
        js = "return action=document.body.scrollHeight"
        count = time // freq
        for i in range(int(count)):
            if self.driver.execute_script(js) >= height + 800:
                return
            sleep(freq)
        raise TimeoutException('scroll_wait error')

    def full_load(self, url, question_num=-1):
        self.driver.delete_all_cookies()
        if self.count >= 100:
            self.reload()
            self.count = 0
        self.count += 1
        self.driver.get(url)
        count = 0
        height = 0
        try:
            more_content = self.driver.find_element_by_class_name('QuestionHeader-detail')
            more_content.click()
        except common.exceptions.NoSuchElementException:
            pass
        except common.exceptions.NoSuchWindowException:
            pass
        js = "return action=document.body.scrollHeight"
        try:
            height = self.driver.execute_script(js)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        except common.exceptions.NoSuchWindowException:
            print('no such window, retrying...')
        if url == start_url:
            count += 10
            msg = 'proccessing %.4f%%' % (count * 100 / question_num)
            print(msg)
        sleep(0.5)

        if url == start_url:
            while True:
                try:
                    height = self.driver.execute_script(js)
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                except common.exceptions.NoSuchWindowException:
                    print('no such window, retrying...')
                try:
                    self.scroll_wait(10, 0.5, height)
                except TimeoutException:
                    print('collecting finished, transmmiting...')
                    break
                count += 10
                msg = 'proccessing %.2f%%' % (count * 100 / question_num)
                print(msg)
            fp = open('log', 'a')
            fp.write('terminate at %.2f%%' % (count * 100 / question_num) + ': question page parsing\n')
            fp.close()
        else:
            if question_num <= 50:
                while height < self.driver.execute_script(js):
                    try:
                        height = self.driver.execute_script(js)
                        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                        sleep(0.5)
                    except common.exceptions.NoSuchWindowException:
                        print('no such window, retrying...')
            else:
                print('parsing big answer...')
                count = 5
                msg = 'proccessing %.4f%%' % (count * 100 / question_num)
                print(msg)
                while True:
                    try:
                        height = self.driver.execute_script(js)
                        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    except common.exceptions.NoSuchWindowException:
                        print('no such window, retrying...')
                    try:
                        self.scroll_wait(10 + int(question_num / 50), 0.5, height)
                    except TimeoutException:
                        break
                    count += 5
                    msg = 'proccessing %.4f%%' % (count * 100 / question_num)
                    print(msg)
                fp = open('log', 'a')
                fp.write('terminate at %.2f%%' % (count * 100 / question_num) + ':answer parsing\n')
                fp.close()
                print('collecting finished, transmmiting...')
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        return self.driver.page_source


def makebase():
    cursor = conn.cursor()
    sql = "create table QA (question_url varchar(60), question varchar(200)," \
          " question_description varchar(200), answerer vchar(255), answer_url varchar(60) primary key," \
          " answer vchar(10000))"
    cursor.execute(sql)
    cursor.close()


def file_write(message):
    try:
        f = codecs.open(file, 'a', 'utf-8')
        f.write(message)
        f.close()
    except IOError:
        print('IOError')
        f = codecs.open(file, 'a', 'utf-8')
        f.write('WARNING: error writing')
        f.close()


def question_parse(url):
    question_path = './question_url'
    response = requests.get(url, headers=headers)
    question_num = int(
        BeautifulSoup(response.content, 'lxml').find_all('strong', class_='NumberBoard-itemValue')[1].string.replace(
            ',', ''))
    if os.path.exists(question_path):
        fp = codecs.open(question_path, 'r', 'utf-8')
        soup = BeautifulSoup(fp.read(), 'lxml')
        fp.close()
    else:
        tmp = firefox.full_load(url, question_num)
        try:
            f = codecs.open(question_path, 'w', 'utf-8')
            f.write(tmp)
            f.close()
        except IOError:
            print('IOError')
            f = codecs.open(question_path, 'w', 'utf-8')
            f.write('WARNING: error writing')
            f.close()
        soup = BeautifulSoup(tmp, 'lxml')
    Checker = set()
    count = 0
    qcount = 0
    print(len(soup.find_all('div', class_='QuestionItem-title')))
    for h in soup.find_all('div', class_='QuestionItem-title'):
        question = h.find_all('a')
        if len(question):
            s = 'https://www.zhihu.com' + question[0]['href']
            n = question[0].string
            if not ((s, n) in Checker):
                QA = QAItem()
                QA.question_url = str(s)
                QA.question = str(n)
                Checker.add((s, n))
                file_write(str(s) + '\n' + str(n) + '\n')  # file write test
                count = answer_parse(s, QA, count)
        file_write('\n\n')  # file write test
        print('\nquestions success at %d' % qcount)
        qcount += 1


def answer_parse(url, question, count):
    response = requests.get(url, headers=headers)
    try:
        answer_num = int(re.findall(r'\d+', BeautifulSoup(response.content, 'lxml').find_all('h4', class_='List'
                                                                                                          '-headerText')[
            0].text)[0])
    except IndexError:
        answer_num = 0
    soup = BeautifulSoup(firefox.full_load(url, answer_num), 'lxml')
    t = soup.find_all('div', class_='QuestionHeader-detail')
    if len(t):
        q = t[0].find_all('span', class_='RichText ztext')
        if len(q):
            file_write(q[0].text + '\n')  # file write test
            if not q[0].text == '':
                question.question_description = str(q[0].text)
            else:
                question.question_description = 'None'
    if len(soup.find_all('div', class_='ContentItem AnswerItem')) == 0:
        question.answer = 'None'
        question.answer_url = question.question_url
        question.answer = 'None'
        question.load()
        msg = 'success at %d' % count
        print(msg)
        count += 1
    else:
        for k in soup.find_all('div', class_='ContentItem AnswerItem'):
            message = k['data-zop']
            question.answerer = str(
                message[message.index('\"authorName\"') + len('\"authorName\":\"'): message.index('\",')])
            question.answer_url = str(
                question.question_url + '/answer/' + message[message.index('itemId\":') + len('itemId'
                                                                                              '\":')
                                                             : message.index(',\"title')])
            file_write(question.answerer + '\n' + question.answer_url + '\n')  # file write test
            a = k.find_all('span', class_='RichText ztext CopyrightRichText-richText')
            if len(a):
                s = a[0].text.replace(' ', '')
                s = s.replace('\n', '')
                file_write(s + '\n')  # file write test
                question.answer = str(s)
                question.load()
                msg = 'success at %d' % count
                print(msg)
                count += 1
    return count


def main():
    global start_url
    global conn
    global file
    global headers
    global firefox

    fp = open('log', 'a')
    fp.write('grabing task begins, time:' + str(time.asctime(time.localtime(time.time()))) + '\n')
    fp.close()
    # test_start_url = 'https://www.zhihu.com/topic/20167298/questions'
    start_url = 'https://www.zhihu.com/topic/19575211/questions'
    # start_url = 'https://www.zhihu.com/topic/19582064/questions'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    file = 'data'
    database = 'sjtu.db'
    conn = sqlite3.connect(database)
    firefox = WebConnector()
    makebase()
    # test_url = 'https://www.zhihu.com/question/19849512'
    tmp = QAItem()
    tmp.question = 'TEST'
    tmp.question_url = 'TEST URL'
    # answer_parse(test_url, tmp, 0)
    try:
        question_parse(start_url)
    except Exception as e:
        fp = open('log', 'a')
        fp.write('Exception occurred at' + str(time.asctime(time.localtime(time.time()))) + ' error:' + str(e) + '\n')
        fp.close()
    try:
        firefox.driver.quit()
    except Exception:
        pass
    try:
        conn.commit()
        conn.close()
    except Exception as e:
        fp = open('log', 'a')
        fp.write('Exception occurred when writing to sql at' + str(
            time.asctime(time.localtime(time.time()))) + 'error:' + str(e) + '\n')
        fp.close()
    fp = open('log', 'a')
    fp.write('grab finished at' + str(time.asctime(time.localtime(time.time()))) + '\n')
    fp.close()


if __name__ == '__main__':
    main()
