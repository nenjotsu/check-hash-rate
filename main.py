

import sys, time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib3
import json
import heapq
import os

is_should_stop = False

class RetryError(Exception):
    pass

def is_down():
    http = urllib3.PoolManager()
    url = 'https://api.nanopool.org/v1/eth/reportedhashrate/<YOUR-ETH-WALLET>'
    response = http.request('GET', url)
    contents = BeautifulSoup(response.data)
    newDictionary = json.loads(str(contents))
    if newDictionary['data'] == 0:
        is_should_stop = True
        os.system("shutdown /r /t 1")
    if newDictionary['data'] > 0:
        # notify("Nanopool", "Miner is Running")
        print 'Miner is Running'
        print str(datetime.now())
        print 'Status'
        print str(newDictionary['status'])
        print 'Hashrate'
        print str(newDictionary['data'])
        is_should_stop = False


def retryloop(attempts, timeout):
    starttime = time.time()
    success = set()
    for i in range(attempts):
        success.add(True)
        yield success.clear
        if success:
            return
        if starttime + timeout < time.time():
            break
    raise RetryError


for retry in retryloop(1000, timeout=60):
    is_down()
    time.sleep(600)

    if is_should_stop == False:
        retry()
