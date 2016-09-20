# coding=utf-8
import requests, bs4, time, re, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlite3 import dbapi2 as sqlite3


# configuration
DATABASE = 'data.db'
DEBUG = True
QUERY = 'select kurs, nazwa, timestamp from note'
INSERT = 'INSERT INTO note (kurs, nazwa, timestamp) ' \
         'VALUES (:kurs, :nazwa, :timestamp)'
DELETE_AGG = 'delete from note_agg'

# ładujemy 20 wystąpień
INSERT_AGG = 'insert into note_agg (nazwa, min_kurs, max_kurs) select nazwa, ' \
             'min(replace(kurs, ",", ".")) as min_kurs, max(replace(kurs, ",", ".")) as max_kurs' \
             ' from note where timestamp in ' \
             '(select DISTINCT timestamp from note order by timestamp desc limit 20) group by nazwa'

# wyciągamy z baze te, które wzrosły o co najmniej 10%
SELECT = 'select nazwa, min_kurs, max_kurs, round(max_kurs-min_kurs,2) ' \
         'as diff_kurs from note_agg' \
         ' where diff_kurs > min_kurs * 0.1'


res = requests.get('http://www.bankier.pl/surowce/notowania')
text = bs4.BeautifulSoup(res.text, "html.parser")

def get_column_data(data_selector, class_value_selector):
    results=[]
    for i in text.findAll(data_selector, class_=class_value_selector):
        # results.append(i.stripped_strings)
        # results.append(i.string)
        results.append(i.text)

    return results


def selector():
    selector_info = {
        "kurs": ["td", re.compile("^colKurs")],
        "nazwa": ["td", re.compile("^colWalor")]
    }
    col_dict = {}

    for key_name, (selector_first, selector_second) in selector_info.iteritems():
        col_dict[key_name] = get_column_data(selector_first, selector_second)

    pivoted_data = pivot_data(col_dict)

    # print("pivoted_data (selector): " + str(pivoted_data).decode('utf8'))

    data_in_db(pivoted_data)

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
        # print("values(pivoted_data): " + str(values))
        cursor.execute(INSERT, values)

    cursor.execute(DELETE_AGG)
    cursor.execute(INSERT_AGG)
    conn.commit()

    get_data()


def get_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    table = cursor.execute(SELECT).fetchall()


    send_mail(table)


def send_mail(table):

    print table

    me = "itop_robot@allegro.pl"
    you = "dawid.lewandowicz@allegrogroup.com"
    msg = MIMEMultipart()
    msg['Subject'] = "Kursy"
    msg['From'] = me
    msg['To'] = you

    part = MIMEText(str(table), 'html', 'utf-8')
    msg.attach(part)

    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo()
    server_ssl.login("dawid.stamdo@gmail.com", "")
    server_ssl.sendmail(me, you, msg.as_string())
    server_ssl.close()

if __name__ == '__main__':
    selector()