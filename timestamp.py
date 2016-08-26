import time
import datetime

timestamp = time.time()

temp = datetime.datetime.fromtimestamp(1471954111).strftime('%Y-%m-%d %H:%M:%S')

print temp
print timestamp
