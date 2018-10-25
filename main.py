from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib3
import json
import heapq
import os


# just holds a function, its arguments, and when we want it to execute.
class TimeoutFunction:
    def __init__(self, function, timeout, *args):
        self.function = function
        self.args = args
        self.startTime = datetime.now() + timedelta(0, 0, 0, timeout)

    def execute(self):
        self.function(*self.args)


# A "todo" list for all the TimeoutFunctions we want to execute in the future
# They are sorted in the order they should be executed, thanks to heapq
class TodoList:
    def __init__(self):
        self.todo = []

    def addToList(self, tFunction):
        heapq.heappush(self.todo, (tFunction.startTime, tFunction))

    def executeReadyFunctions(self):
        if len(self.todo) > 0:
            tFunction = heapq.heappop(self.todo)[1]
            while tFunction and datetime.now() > tFunction.startTime:
                #execute all the functions that are ready
                tFunction.execute()
                if len(self.todo) > 0:
                    tFunction = heapq.heappop(self.todo)[1]
                else:
                    tFunction = None
            if tFunction:
                #this one's not ready yet, push it back on
                heapq.heappush(self.todo, (tFunction.startTime, tFunction))


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def singleArgFunction(x):
    http = urllib3.PoolManager()
    url = 'https://api.nanopool.org/v1/eth/reportedhashrate/0x6ab7d21de169cbfc81afb1e5f1cd79d3e373e9ef'
    response = http.request('GET', url)
    contents = BeautifulSoup(response.data)
    newDictionary = json.loads(str(contents))
    if newDictionary['status'] == False:
        print 'Miner is Down or you do not have internet'
        os.system("shutdown /r /t 1")
    if newDictionary['status'] == True:
        notify("Nanopool", "Miner is Running")
        print 'Miner is Running'
        print 'Status'
        print str(newDictionary['status'])
        print 'Hashrate'
        print str(newDictionary['data'])


def multiArgFunction(x, y):
    #Demonstration of passing multiple-argument functions
    print '==> End'


# Make some TimeoutFunction objects
# timeout is in milliseconds
a = TimeoutFunction(singleArgFunction, 600000, 20)
# b = TimeoutFunction(multiArgFunction, 2000, *(11, 12))
# c = TimeoutFunction(quit, 3000, None)

todoList = TodoList()
todoList.addToList(a)
# todoList.addToList(b)
# todoList.addToList(c)

while True:
    todoList.executeReadyFunctions()
