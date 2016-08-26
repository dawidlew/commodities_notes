# coding=utf-8
import requests, bs4, time, re

from sqlite3 import dbapi2 as sqlite3

res = requests.get('http://www.bankier.pl/surowce/notowania')
soup = bs4.BeautifulSoup(res.text, "html.parser")
i = soup.findAll("td", class_=re.compile("^colWalor"))
j = soup.findAll("td", class_=re.compile("^colKurs"))

print i
print j


