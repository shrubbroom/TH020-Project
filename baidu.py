from aip import AipNlp
import time
from db2xlsx import *
from sqlio import *

APP_ID = "-"
API_KEY = "-"
SECRET_KEY = "-"

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# text="SJTU就这点格局。开个暑期学校连PPT都设置密码，还美其名曰只给参加的人开放，不给不参加想免费获得资料的同学。懒得diss了，大佬离开去清北是对的。 "
# result=client.sentimentClassify(text)
#
# print(result)
# {'log_id': 8570377247136157270,
# 'text': 'SJTU就这点格局。开个暑期学校连PPT都设置密码，还美其名曰只给参加的人开放，不给不参加想免费获得资料的同学。懒得diss了，大佬离开去清北是对的。 ',
# 'items': [{'positive_prob': 0.139645, 'confidence': 0.689679, 'negative_prob': 0.860355, 'sentiment': 0}]}

if __name__ == '__main__':
    database = SqlIO("sjtu.db")
    table_name = 'QA_sentiment'
    terms = ['positive_prob', 'confidence', 'negative_prob', 'sentiment', 'question']
    question_pre = {}
    if database.SqlTableExists(table_name):
        question_pre = set(database.SqlReader(table_name, "question"))
        print('read former content from ' + table_name)
    else:
        database.SqlMake(table_name, "id", 100, terms, 40)

    # if database.SqlTableExists(table_name):
    #     database.SqlDeletetable(table_name)
    #     print('delete ' + table_name)
    # database.SqlMake(table_name, "id", 100, terms, 40)

    question_all = set(database.SqlReader("QA", "question"))
    # sentiment_result_all=[]
    count = 0

    for question in question_all:
        if question not in question_pre:
            time.sleep(0.51)
            sentiment_result = client.sentimentClassify(question)
            # sentiment_result_all.append(sentiment_result)
            count += 1
            print()
            print(count)
            print(question)
            print(sentiment_result)
            # print(sentiment_result['items'][0]['positive_prob'])
            # try:
            data = {'id': count, \
                    'positive_prob': sentiment_result['items'][0]['positive_prob'], \
                    'confidence': sentiment_result['items'][0]['confidence'], \
                    'negative_prob': sentiment_result['items'][0]['negative_prob'], \
                    'sentiment': sentiment_result['items'][0]['sentiment'], \
                    'question' : question}
            database.SqlInsert(table_name, data)
            # except KeyError as e:
            #     print('request limit reached')
            #     print(str(e))

            # if count>10:
            #     break




    print('sentiment analyze finished')
    # db2xls('./filter2.db')
