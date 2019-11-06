import xml
import requests
import re
from bs4 import BeautifulSoup
from lxml import html

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
Checker = set()


def QuestionParser(url):
    Qresponse = requests.get(url, headers=headers,)
    print(url)
    Qsoup = BeautifulSoup(Qresponse.content, "lxml")
    for k in Qsoup.find_all('div', class_='ContentItem AnswerItem'):
        a = k.find_all('span', class_='RichText ztext CopyrightRichText-richText')
        if len(a):
            s = a[0].text.replace(' ', '')
            s = s.replace('\n', '')
            print(s)
            print('\n')


url = 'https://www.zhihu.com/topic/20167298/hot'

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

for h in soup.find_all('h2', class_='ContentItem-title'):
    question = h.find_all('meta')
    if len(question):
        s = question[0]['content']
        n = question[1]['content']
        if not ((s, n) in Checker):
            Checker.add((s, n))
            print(n)
            QuestionParser(s)