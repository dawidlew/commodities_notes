# coding=utf-8
import requests, bs4, time, re
from sqlite3 import dbapi2 as sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DATABASE = 'data.db'
DEBUG = True
SELECT = 'select nazwa, min_kurs, max_kurs, round(max_kurs-min_kurs,2) ' \
         'as diff_kurs from note_agg' \
         ' where diff_kurs > min_kurs * 0.1'


res = requests.get('http://www.bankier.pl/surowce/notowania')
text = bs4.BeautifulSoup(res.text, "html.parser")


def get_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # results=[]
    # for i in text.findAll(data_selector, class_=class_value_selector):
    #     results.append(i.text)

    table = cursor.execute(SELECT).fetchall()

    send_mail(table)


def send_mail(table):

    print str(table)

    me = "itop_robot@allegro.pl"
    you = "dawid.lewandowicz@allegrogroup.com"
    msg = MIMEMultipart()
    msg['Subject'] = "Kursy test"
    msg['From'] = me
    msg['To'] = you

    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="https://www.python.org">link</a> you wanted.
        </p>
      </body>
    </html>
    """
    part = MIMEText(str(table), 'html', 'utf-8')

    msg.attach(part)

    s = smtplib.SMTP('smtp.qxlint')
    s.sendmail(me, you, msg.as_string())
    s.quit()


if __name__ == '__main__':
    get_data()