import sqlite3 as sqlite
from sqlio import *
from db2xlsx import *
import os

def list2db(list,tbl_name):
    print('input:')
    print(list)

    db=SqlIO(tbl_name+'.db')
    if db.SqlTableExists(tbl_name):
        print('The table has already existed.')
        print('Are yor sure to delete table: '+tbl_name)
        print('print "yes" to comfirm deletion, otherwise deletion would be canceled.')
        print('----------------------------------------------------------------')
        delete_or_not=input()
        print('----------------------------------------------------------------')
        if delete_or_not=='yes':
            db.SqlDeletetable(tbl_name)
        else:
            print("Stop list2db.")
            print("Please check your table name.")
            return False
    db.SqlMake(tbl_name,tbl_name,100,[],0)
    data={}
    for item in list:
        data[tbl_name]=str(item)
        db.SqlInsert(tbl_name,data)
        print('insert '+str(item))

    print('finish')
    return True

def list2xls(list,tbl_name):
    if(list2db(list,tbl_name)):
        db2xls('./'+tbl_name+'.db')

if __name__ == '__main__':
    examples=[1,2,3,4,5,6]
    list2xls(examples,'examples')

