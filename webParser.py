from lxml import html
import requests
import time
import re
import os
from bs4 import BeautifulSoup


htmlLink = "https://api.ethermine.org/miner/0x39107bD9e31f284f819e68bC302128b11B0c7bdB/currentStats"

# These can be increased, and changed based on the number of active graphics cards
# The number represents the amount of MH/s
thresholdTwo = 45
thresholdOne = 20
#
# number = int(input("How many graphics cards are on? \n"))
number = 1

def webParser(htmlLink):

    page = requests.get(htmlLink)
    print(page)

    c = page.content
    soup = BeautifulSoup(c, "html.parser")

    # print(soup.prettify())

    spanner = (re.search("\"reportedHashrate\":", soup.prettify()).span()[1])
    spanned = re.search(",", soup.prettify()[spanner:]).span()[0]

    print("Reported Hashrate: ", soup.prettify()[spanner:spanner+spanned])

    RHR_M = str(soup.prettify()[spanner:spanner+spanned])

    throughput = int(RHR_M)

    alert(throughput, number)

def alert(throughput, numb):

    # This first if sentence is used when utilizing one or more of the graphics cards for something else than ethermine
    if throughput < thresholdOne and numb == 1:
        # Explainations exist in the elif sentance
        
        os.system("TASKKILL /F /IM cmd.exe")
        os.startfile("start.bat")
        
        # Will eventually play an alert on the phone to alert the user
        # Alert
        
    # When both of the graphics cards are used for ethermining
    elif throughput < thresholdTwo and numb ==2:
        # os.system kills the commandlines, used for mining
        os.system("TASKKILL /F /IM cmd.exe")
        # os.startfile starts the ethereum miner
        os.startfile("start.bat")
        # I have not included an alert sound yet, but am considering doing this for android
        # print("Play alert, do not care which type of alert could be anything")



def clock():

    # This is used for refreshing and rechecking the throughput
    while True:
        print("Clock ...")
        webParser(htmlLink)
        time.sleep(600)

clock()