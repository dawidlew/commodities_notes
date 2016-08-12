# coding=utf-8
import requests, bs4
import time
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack


# configuration
DATABASE = 'data.db'
DEBUG = True
QUERY = 'select name, city, round(avg(price_min),2) as price_min, round(avg(price_max),2) as price_max ' \
        'from note where timestamp in (select timestamp from note group by timestamp ' \
        'order by timestamp desc limit 50) group by name, city'
INSERT = 'INSERT INTO note (kurs, nazwa, timestamp) ' \
         'VALUES (:kurs, :nazwa, :timestamp)'


res = requests.get('http://www.bankier.pl/surowce/notowania')
text = bs4.BeautifulSoup(res.text, "html.parser")

def get_column_data(data_selector, class_value_selector):
    results=[]
    for i in text.find_all(data_selector, class_=class_value_selector):
        results.append(i.string)
    return results


def selector():
    selector_info = {
        "kurs": ["td", "colKurs change down"],
        "nazwa": ["td", "colWalor textNowrap"]
    }
    col_dict = {}
    for key_name, (selector_first, selector_second) in selector_info.iteritems():
        col_dict[key_name] = get_column_data(selector_first, selector_second)

    pivoted_data = pivot_data(col_dict)

    print("pivoted_data (selector): " + str(pivoted_data))

    # data_in_db(pivoted_data)

def pivot_data(col_dict, timestamp=time.time()):
    output = []
    first_key_name = col_dict.keys()[0]

    # print("first_key_name: " + str(first_key_name))

    values_column_len = len(col_dict[first_key_name])

    # print("values_column_len: " + str(values_column_len))

    for value_no in range(values_column_len):
        row_data = {}
        for key in col_dict.keys():
            row_data[key] = col_dict[key][value_no]
        row_data['timestamp'] = int(timestamp)
        output.append(row_data)

    # print("output (pivot_data): " + str(output))

    return output



def data_in_db(pivoted_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # print("pivoted_data (data_in_db):: " + str(pivoted_data))

    for values in pivoted_data:

        # print("values ( for pivoted_data): " + str(values))

        cursor.execute(INSERT, values)
    conn.commit()

    results = conn.execute("select kurs, nazwa, timestamp from note")
    print("results:" + str(results.fetchall()))


if __name__ == '__main__':
    selector()