from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from multiprocessing import Process
import requests
import time
import sys


proxylist = []
ValidPRXlist = []

txt = input("Message to send:\n$ ")
n = int(input("how many messages from each thread?\n$ "))


def GetProxy():
    def checkProxy(ProxyQ):
        try:
            resp = requests.get("https://icanhazip.com/", proxies={'http': ProxyQ})
            return (True)
        except:
            return (False)
    with open("proxylist.txt", 'r') as PrxFile:
        proxylist = PrxFile.readlines()
    if not proxylist:
        print ("The proxies file is empty!")
        sys.exit()
    k = 0
    for k in proxylist:
        booli = checkProxy(k.strip('\n'))
        if booli is False:
            print (("The Proxy: " + k.strip('\n') + " is not valid"))
            proxylist.remove(k)
    return (proxylist)


def SetProxy(proxylist, numi):
    PROXY = proxylist[numi - 1]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
    return (chrome_options)


def WorkIT(num):
    global ValidPRXlist
    chrome_options = SetProxy(ValidPRXlist, num)
    a = webdriver.Chrome('drivers/chromedriver' + str(num), chrome_options=chrome_options)
    a.get("https://web.whatsapp.com")
    time.sleep(17 * len(ValidPRXlist))

    found = False
    while (not found):
        try:
            textarea = a.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            found = True
        except:
            print("Please press the desired chat..")
            time.sleep(5)
        pass
    print("Chat found!")
    for i in range(n):
        textarea.send_keys(txt)
        #time.sleep(1)
        textarea.send_keys(Keys.RETURN)
        print (i)


if __name__ == "__main__":
    ValidPRXlist = GetProxy()
    print ("You have "+str(len(ValidPRXlist)) + " thread(s)")
    if not ValidPRXlist:
        print ("Your proxy(s) is not valid")
        sys.exit()
    proc = []
    for i in range(len(ValidPRXlist)):
        p = Process(target=WorkIT, args=(i + 1, ))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

