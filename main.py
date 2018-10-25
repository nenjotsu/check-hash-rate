import sys, time
from datetime import datetime
from bs4 import BeautifulSoup
import urllib3
import json
import os

is_continue = True


class RetryError(Exception):
    pass


def is_down():
    http = urllib3.PoolManager()
    url = 'https://api.nanopool.org/v1/eth/reportedhashrate/<YOUR-ETH-WALLET>'
    response = http.request('GET', url)
    contents = BeautifulSoup(response.data)
    newDictionary = json.loads(str(contents))
    if newDictionary['data'] == 0:
        os.system("shutdown /r /t 1")
    if newDictionary['data'] > 0:
        print 'Miner is Running'
        print 'DateTime: ' + str(datetime.now())
        print 'Status: ' + str(newDictionary['status'])
        print 'Reported Hashrate: ' + str(newDictionary['data'])
        print '===================================='


def retryloop(attempts, timeout):
    starttime = time.time()
    success = set()
    for _ in range(attempts):
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

    if is_continue:
        retry()
