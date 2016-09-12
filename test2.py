# coding=utf-8
import requests, bs4, time, re, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlite3 import dbapi2 as sqlite3
import html
import HTML


DATABASE = 'data.db'


conn = sqlite3.connect(DATABASE)

cur = conn.cursor()

#mysql query

query = ('select nazwa, min_kurs, max_kurs, round(max_kurs-min_kurs,2) '
         'as diff_kurs from note_agg'
         ' where diff_kurs > min_kurs * 0.1')

cur.execute(query)

rows = cur.fetchall()

# for row in rows:
#     for col in row:
#         print  '<TR> <TD>' + str(col) + '</TD> </TR>'


htmlcode = HTML.table(str(rows))


print htmlcode


me = "itop_robot@allegro.pl"
you = "dawid.lewandowicz@allegrogroup.com"
msg = MIMEMultipart()
msg['Subject'] = "Kursy test2"
msg['From'] = me
msg['To'] = you

part = MIMEText(htmlcode, 'html', 'utf-8')
msg.attach(part)

s = smtplib.SMTP('smtp.qxlint')
s.sendmail(me, you, msg.as_string())
s.quit()

