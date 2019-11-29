import sqlite3 as sqlite
from sqlio import *
from db2xlsx import *


if __name__ == '__main__':
    # database=SqlIO('sjtu.db')
    # filter_before='make_sjtu_great_again'
    # filter_after='filter'
    # filter="select * from "+filter_before+" where \
    #         (question like '如何评价%' or\
    #         question like '如何看待%')and\
    #         (question like '%上海交通大学%' or\
    #         question like '%交大%' or\
    #         question like '%上交%')and\
    #          (question not like '%高考%)"
    #
    # if not database.SqlTableExists(filter_after):
    #     database.SqlMake(filter_after)

    database=SqlIO('sjtu.db')
    filter_after='make_sjtu_great_again_again_filter'
    filter_before='make_sjtu_great_again_again'

    filter="select * from "+filter_before+" where \
            (question like '如何评价%' or\
            question like '如何看待%')and\
            (question like '%上海交通大学%' or\
            question like '%交大%' or\
            question like '%上交%')and\
             (question not like '%高考%')"

    # sql='select question_url,make_sjtu_great_again.question,follower,viewed,date,answers, \
    #     positive_prob,confidence,negative_prob,sentiment\
    #     from make_sjtu_great_again left join QA_sentiment on \
    #     make_sjtu_great_again.question=QA_sentiment.question'

    terms=['question_url','question','follower','viewed','date','answers', \
        'positive_prob','confidence','negative_prob','sentiment']
    terms_without_primary=terms.copy()
    primary=terms_without_primary.pop(0)

    if database.SqlTableExists(filter_after):
        database.SqlDeletetable(filter_after)
    database.SqlMake(filter_after,primary,100,terms_without_primary,500)
    tmp_table=database.Sqlexecute(filter)
    count=0
    for row in tmp_table:
        count+=1
        print()
        print(count)
        print(row[1])
        data={}
        # data['question_url']=row[0]
        # data['question'] = row[0]
        # data['follower'] = row[0]
        # data['viewed'] = row[0]
        # data['date'] = row[0]
        # data['answers'] = row[0]
        # data['positive_prob'] = row[0]
        # data['confidence'] = row[0]
        # data['negative_prob'] = row[0]
        # data['question_url'] = row[0]
        # data['question_url'] = row[0]

        for i in range(len(terms)):
            data[terms[i]]=row[i]
        database.SqlInsert(filter_after,data)

    print('finish')


