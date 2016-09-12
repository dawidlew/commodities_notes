# coding=utf-8
import requests, bs4, time, re
from sqlite3 import dbapi2 as sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import rows as rows
import html

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

    table = cursor.execute(SELECT).fetchall()
    print table
    send_mail(table)


def send_mail(table):

    # print str(table)

    html = """
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>html title</title>
  <style type="text/css" media="screen">
    table{
        background-color: #AAD373;
        empty-cells:hide;
    }
    td.cell{
        background-color: white;
    }
  </style>
</head>
<body>
  <table style="border: blue 1px solid;">
    <tr><td class="cell">Cell 1.1</td><td class="cell">Cell 1.2</td></tr>
    <tr><td class="cell">Cell 2.1</td><td class="cell"></td></tr>
  </table>
</body>
"""

    me = "itop_robot@allegro.pl"
    you = "dawid.lewandowicz@allegrogroup.com"
    msg = MIMEMultipart()
    msg['Subject'] = "Kursy test"
    msg['From'] = me
    msg['To'] = you

    part1 = MIMEText(html, 'html', 'utf-8')
    part2 = MIMEText(html, 'html', 'utf-8')
    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.qxlint')
    s.sendmail(me, you, msg.as_string())
    s.quit()


if __name__ == '__main__':
    get_data()
