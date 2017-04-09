#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""morphological analysis."""

import csv
import MeCab
# import numpy as np
import pymysql

csv_file_path = '/tmp/morphological_analysis.csv'
select_sql = 'SELECT ' \
    'item_no, object_class, protocol, description ' \
    'FROM scrapy.scp;'
insert_sql = 'INSERT INTO ' \
    'scrapy.morphological_analysis(item_no, word, description) ' \
    'VALUES (%s, %s, %s);'

# mecab tagger
tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

# open csv file
fp = open(csv_file_path, 'w')
writer = csv.writer(fp, lineterminator='\n')

# connect DB
conn = pymysql.connect(
    host='127.0.0.1',
    unix_socket='/tmp/mysql.sock',
    user='root',
    passwd='',
    db='mysql',
    charset='utf8',
    cursorclass=pymysql.cursors.SSCursor
)
cur = conn.cursor()

# select from DB
cur.execute(select_sql)
mysql_results = cur.fetchall()
for mysql_result in mysql_results:
    words_to_db = []
    words_to_csv = []

    # morphological analysis
    mecab_results = tagger.parse(mysql_result[2]).split('\n')
    for mecab_result in mecab_results:
        # EOS
        if mecab_result == 'EOS' or mecab_result == '':
            continue

        # check word class
        tmp = mecab_result.split('\t')
        if not tmp[1].startswith('名詞,'):
            continue
        if len(tmp[0]) <= 1:
            continue

        # append to list
        words_to_db.append((mysql_result[0], tmp[0], tmp[1]))
        words_to_csv.append(tmp[0])

    # write to csv file
    if len(words_to_csv) >= 1:
        # words_to_csv = np.unique(words_to_csv).tolist()
        words_to_csv.insert(0, mysql_result[0])
        writer.writerow(words_to_csv)

# close csv file
fp.close()

# insert into DB
try:
    cur.executemany(insert_sql, words_to_db)
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()

# close DB connection
conn.close()
