#html web scraper of valorant tracker.gg profile that presents games played and hours by category, along with the sum totals
#made by Sung Mo Yang

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui as gui
import os, sys

username = None
username = gui.prompt("Please enter your RIOT ID and tagline\n\n (EX: jett#1234)", "Hours Playing Valorant via Tracker.gg", "")

if username == None:
    quit()
if username == "":
    gui.alert("Invalid RIOT ID", "Hours Playing Valorant via Tracker.gg")
    quit()

nameChar = username.split("#")
if len(nameChar) != 2:
    gui.alert("Invalid RIOT ID", "Hours Playing Valorant via Tracker.gg")
    quit()
if len(nameChar[0]) > 16 or len(nameChar[0]) <= 0:
    gui.alert("Invalid RIOT ID", "Hours Playing Valorant via Tracker.gg")
    quit()
if len(nameChar[1]) > 5 or len(nameChar[0]) <= 0:
    gui.alert("Invalid RIOT ID", "Hours Playing Valorant via Tracker.gg")
    quit()

compURL = "https://tracker.gg/valorant/profile/riot/"+nameChar[0]+"%23"+nameChar[1]+"/overview?playlist=competitive&season=all"
dmURL = "https://tracker.gg/valorant/profile/riot/"+nameChar[0]+"%23"+nameChar[1]+"/overview?playlist=deathmatch&season=all"
esclURL = "https://tracker.gg/valorant/profile/riot/"+nameChar[0]+"%23"+nameChar[1]+"/overview?playlist=escalation&season=all"
replURL = "https://tracker.gg/valorant/profile/riot/"+nameChar[0]+"%23"+nameChar[1]+"/overview?playlist=replication&season=all"
snowURL = "https://tracker.gg/valorant/profile/riot/"+nameChar[0]+"%23"+nameChar[1]+"/overview?playlist=snowball&season=all"
spikeURL = "https://tracker.gg/valorant/profile/riot/"+nameChar[0]+"%23"+nameChar[1]+"/overview?playlist=spikerush&season=all"
unratedURL = "https://tracker.gg/valorant/profile/riot/"+nameChar[0]+"%23"+nameChar[1]+"/overview?playlist=unrated&season=all"

URLs = [compURL, dmURL, esclURL, replURL, snowURL, spikeURL, unratedURL]
hoursArray = []
strParsearray = []

userExists = False

try: 
    driver = webdriver.Chrome(ChromeDriverManager().install())
except:
    gui.alert("Error loading website", "Hours Playing Valorant via Tracker.gg")
    driver.quit()
    quit()

for url in URLs:
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    try: 
        hoursText = soup.find("span", {"class":"playtime"}).text
    except:
        if userExists:
            hoursArray.append(['0h'])
            continue
        else:
            for url in URLs:
                driver.get(url)
                html = driver.page_source
                soup = BeautifulSoup(html, features="html.parser")
                try:
                    hoursText = soup.find("span", {"class":"playtime"}).text
                except:
                    pass
                else:
                    userExists = True
            if userExists:
                hoursArray.append(['0h'])
                continue
            else:
                gui.alert("Could not find account on Tracker.gg", "Hours Playing Valorant via Tracker.gg")
                driver.quit()
                quit()
    else:
        hoursTextArray = hoursText.split(' ')
        hoursTextArray = hoursTextArray[10::]

        for i in hoursTextArray:
            if i == "Play":
                break
            else:
                strParsearray.append(i)
        hoursArray.append(strParsearray)
        strParsearray=[]
        userExists = True

totalHours, totalMin, totalSec = 0, 0, 0

labelCounter = 0
labelMap = {0:"Competitive:  ", 1:"Deathmatch:  ", 2:"Escalation:     ", 3:"Replication:   ", 4:"Snowball:      ", 5:"Spike Rush:   ", 6:"Unrated:        ", 7:"Total:         "}
printStringFinal =""


for time in hoursArray:
    hoursNum, minNum, secNum = 0, 0, 0

    for sect in time:
        match sect[-1]:
            case 'h':
                hoursNum = int(sect[:-1])
                continue
            case 'm':
                minNum = int(sect[:-1])
                continue
            case 's':
                secNum = int(sect[:-1])
                continue
            case _:
                continue
    printString = labelMap[labelCounter]+ str(hoursNum)+" hours, "+ str(minNum)+" minutes, "+ str(secNum)+" seconds\n"
    printStringFinal += (printString)
    printStringFinal += "\n"

    totalHours+=hoursNum
    totalMin+=minNum
    totalSec+=secNum

    labelCounter+=1

printStringFinal += "\n\n"

while(True):
    if (totalSec // 60) >= 1:
        totalSec = totalSec//60
        totalMin += 1
    else:
        break

while(True):
    if (totalMin // 60) >= 1:
        totalMin = totalMin//60
        totalHours += 1
    else:
        break

printString = labelMap[labelCounter]+ str(totalHours)+" hours, "+ str(totalMin)+" minutes, "+ str(totalSec)+" seconds\n"
printStringFinal += (printString)

driver.quit()
gui.alert(printStringFinal, "Hours Playing Valorant via Tracker.gg")