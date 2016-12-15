# coding: utf8
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def fetch_one():
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tourdb", charset="utf8")
    cursor = db.cursor()
    sql = 'select * from tourqa where score is null ORDER BY rand();'
    cursor.execute(sql)
    res = cursor.fetchone()
    db.close()
    return res


def update_score(idx, score):
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="tourdb", charset="utf8")
    cursor = db.cursor()
    sql = 'update tourqa set score = {} where id = {};'.format(score, idx)
    cursor.execute(sql)
    db.commit()
    db.close()


def insert_qapair(title, answer, pubtime, query, score):
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="cqa", charset="utf8")
    cursor = db.cursor()
    cursor.execute('insert into tourqa(title, answer, pubtime, query, score) values \
                   (%s, %s, %s, %s, %s)', (title, answer, pubtime, query, score))
    db.commit()
    db.close()
