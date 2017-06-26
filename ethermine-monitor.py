from lxml import html
import requests
import time
import re
import os



htmlLink = "https://ethermine.org/miners/0x39107bD9e31f284f819e68bC302128b11B0c7bdB" # append your mineraddress after the last slash

# These can be increased, and changed based on the number of active graphics cards
# The number represents the amount of MH/s
thresholdTwo = 45
thresholdOne = 20

number = int(input("How many graphics cards are on? \n"))

def webParser(htmlLink, number):

    page = requests.get(htmlLink)

    tree = html.fromstring(page.content)

    graph = tree.xpath('/html/body/div[1]/div/div[2]/script[7]/text()')

    length = len(graph[0])
    end = graph[0][length - 78:length - 1]

    # The index of the reported hashrates doble quote (in the html code)
    endInd = int(re.search('\"RHR_M\"', end).span()[1])

    # The actual number containing the hashrate which the PC reports, given that said PC reports the hashrate
    RHR_M = str(end[endInd+1:endInd+3])


    print("")
    print("Reported Hashrate: ")
    print(RHR_M)

    throughput = int(RHR_M)

    alert(throughput, number)
    return throughput

def alert(throughput, numb):

    # This first if sentence is used when utilizing one or more of the graphics cards for something else than ethermine
    if throughput < thresholdOne and numb == 1:
        # Explainations exist in the next if sentance
        os.system("TASKKILL /F /IM cmd.exe")
        os.startfile("start.bat")
        print("Play alert, do not care which type of alert could be anything")

    # When all of the graphics cards are used for ethermining
    elif throughput < thresholdTwo and numb ==2:
        # os.system kills the commandlines, used for mining
        os.system("TASKKILL /F /IM cmd.exe")
        # os.startfile starts the ethereum miner
        os.startfile("start.bat")
        # I have not included an alert sound yet, but am considering doing this for android
        print("Play alert, do not care which type of alert could be anything")



def clock():

    # This is used for refreshing and rechecking the throughput
    while True:
        print("Clock ...")
        webParser(htmlLink, number)
        time.sleep(600)

clock()