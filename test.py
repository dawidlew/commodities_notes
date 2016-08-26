import smtplib

server = smtplib.SMTP('smtp.qxlint')
server.sendmail('itop@allegro.pl', 'dawid.lewandowicz@allegrogroup.com', 'tekst')
server.quit()