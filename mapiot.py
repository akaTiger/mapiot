import requests
import json

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def minecraftColorcodeTranslate(letter):
    mcFontDict = {
        "DARK_RED": ["\u00A74", "&4"],
        "RED": ["\u00A7c", "&c"],
        "GOLD": ["\u00A76", "&6"],
        "YELLOW": ["\u00A7e", "&e"],
        "DARK_GREEN": ["\u00A72", "&2"],
        "GREEN": ["\u00A7a", "&a"],
        "AQUA": ["\u00A7b", "&b"],
        "DARK_AQUA": ["\u00A73", "&3"],
        "DARK_BLUE": ["\u00A71", "&1"],
        "BLUE": ["\u00A79", "&9"],
        "LIGHT_PURPLE": ["\u00A7d", "&d"],
        "DARK_PURPLE": ["\u00A75", "&5"],
        "WHITE": ["\u00A7f", "&f"],
        "GRAY": ["\u00A77", "&7"],
        "DARK_GRAY": ["\u00A78", "&8"],
        "BLACK": ["\u00A70", "&0"],
        "FONT_RESET": ["\u00A7r", "&r"],
        "FONT_BOLD": ["\u00A7l", "&l"],
        "FONT_ITALIC": ["\u00A7o", "&o"],
        "FONT_UNDERLINE": ["\u00A7n", "&n"],
        "FONT_STRIKE": ["\u00A7m", "&m"]
    }
    for colorCodes in mcFontDict.keys():
        letter = letter.replace(mcFontDict[colorCodes][0], mcFontDict[colorCodes][1])
    letter = letter.replace("&gt;&gt;&gt;", ">>>")
    return letter
        
def formatUUID(uuid):
    outLst = [alphabit for alphabit in uuid if alphabit != "-"]
    return "".join(outLst)

def testUUID(uuid):
    fullURL = "https://api.minetools.eu/profile/" + uuid
    content = requests.get(url=fullURL)
    result = json.loads(content.text)
    if str(result["decoded"]) == "None":
        return False
    else:
        return True

def whatToDo():
    mapiotFunc = [
            "UUID",
            "serverIP",
            "slimeChecker"
        ]
    for func in mapiotFunc:
        print(f"[{mapiotFunc.index(func)}] {func}")
    userCall = input("Choose what to do:")
    try:
        userCall = int(userCall)
        return mapiotFunc[userCall]
    except:
        print("Invalid input. Quitting...")
        quit()

def checkPWD(pwd):
        if pwd[-1] != "/":
            pwd = pwd + "/"
            return pwd
        else:
            return pwd

def resultSavePWD():
    saveDir = input("Image save PATH, enter 0 goes default(./): ")
    saveFileName = input("Image filename, enter 0 goes default('slimeResult'):")
    if saveFileName == "0":
        saveFileName = "slimeResult"
    if saveDir == "0":
        fullDir = saveFileName + ".png"
        return fullDir
    else:
        if not os.path.exists(saveDir):
            yesNoCreatePath = input("Unknown path, create it? [y/N]")
            if yesNoCreatePath == "y":
                os.makedirs(saveDir)
                saveDir = checkPWD(saveDir)
                fullDir = saveDir + saveFileName + ".png"
                return fullDir
            else:
                print("Quitting...")
                quit()
        else:
            saveDir = checkPWD(saveDir)
            fullDir = saveDir + saveFileName + ".png"
            return fullDir

def playerAPI():
    infoIn = input("Type in player UUID, accept any form:\n")
    toolDict = {
            "MoJangAPI": "https://api.mojang.com/user/profiles/",
            "MineToolsEU": "https://api.minetools.eu/profile/"
        }
    while True:
        if testUUID(infoIn) is False:
            infoIn = input("Invalid UUID, enter again or 'q' to quit:\n")
            if infoIn == "q":
                quit()
        else:
            break
    dumpLst = []
    for tool in toolDict.keys():
        if tool == "MoJangAPI":
            infoNeeded = formatUUID(infoIn)
            FullURL = toolDict[tool] + infoNeeded + "/names"
            content = requests.get(url=FullURL)
            nameLst = json.loads(content.text)
            if len(nameLst) > 1:
                infoA = "Current ID: " + nameLst[-1]["name"]
                previousName = []
                for name in nameLst[:-1]:
                    previousName.append(name["name"])
                infoB = "Used IDs: " + "; ".join(previousName)
            if len(nameLst) == 1:
                infoA = "ID: " + nameLst[0]["name"]
        else:
            fullURL = toolDict[tool] + infoIn
            content = requests.get(url=fullURL)
            formated = json.loads(content.text)
            dumpLst.append([tool, formated])
    print("-=" * 15)
    print(infoA)
    print(infoB)
    print("Cape URL:", dumpLst[0][1]["decoded"]["textures"]["CAPE"]["url"])
    print("Skin URL:", dumpLst[0][1]["decoded"]["textures"]["SKIN"]["url"])
    print("-=" * 15)

def serverAPI():
    infoIn = input("Server IP address:\n")
    gamePort = int(input("Server port:\n"))
    print("Lookup in progress...")
    toolDict = {
        "mcsrvstat": "https://api.mcsrvstat.us/2/",
        "mcapi": "https://mcapi.us/server/status?ip=",
    }
    dumpLst = []
    if gamePort == 0:
        for tool in toolDict.keys():
            fullURL = toolDict[tool] + infoIn
            content = requests.get(url=fullURL)
            formated = json.loads(content.text)
            dumpLst.append([tool, formated])

    if dumpLst[0][1]["online"] == True:
        print("-=" * 15)
        print("Stat:", "Serving")
        print("Ping:" , f"{int(dumpLst[1][1]['duration']) / 1000000:.2f} 毫秒")
        print("IP:", f"{dumpLst[0][1]['hostname']} ({dumpLst[0][1]['ip']})")
        print("Port:", dumpLst[0][1]["port"])
        print("Motd Line A:", minecraftColorcodeTranslate(dumpLst[0][1]["motd"]["clean"][0]).strip())
        print("Motd Line B:", minecraftColorcodeTranslate(dumpLst[0][1]["motd"]["clean"][1]).strip())
        print("Players:", f"{dumpLst[0][1]['players']['online']} / {dumpLst[0][1]['players']['max']}")
        print("-=" * 15)
    else:
        print("-=" * 15)
        print("IP:", f"{dumpLst[0][1]['hostname']} ({dumpLst[0][1]['ip']})")
        print("Stat:", "Not Serving")
        print("-=" * 15)

def slimeChunckFinder():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--headless')
    options.add_argument('test-type')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "enable-automation"])
    print("Init headless Chrome...")
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    baseURL = "http://mineatlas.com/?levelName=Random&seed="
    seedInput = input("Minecraft seeds:\n")
    locationX = "&mapCentreX=" + input("Location X:\n")
    locationY = "&mapCentreY=" + input("Location Y:\n")
    uselessArg = [
        "&mapZoom=18",
        "&pos=",
        "&Player=true",
        "&Spawn=true",
        "&Likely+Villages=false",
        "&Ocean+Monuments=false",
        "&Jungle+Temples=false",
        "&Desert+Temples=false",
        "&Witch+Huts=false",
        "&Slime+Chunks=true"
    ]
    otherAttri = ''.join(uselessArg)
    driver.get(baseURL + seedInput + locationX + locationY + otherAttri)
    print("Visiting Mineatlas... Wait for 15 seconds...")
    time.sleep(15)
    slimeCanvas = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div[2]')
    fileDir = resultSavePWD()
    slimeCanvas.screenshot(fileDir[:])
    driver.quit()
    print("Image processing...")
    slimeCanvasScreenShot = Image.open(fileDir[:])
    originalWidth, originalHeight = slimeCanvasScreenShot.size
    width = originalWidth / 2 - 40
    top = originalWidth / 2 - 40
    right = originalHeight / 2 + 40
    bottom = originalHeight / 2 + 40
    slimeResult = slimeCanvasScreenShot.crop((width, top, right, bottom))
    slimeResult.save(fileDir[:])
    print("Result saved to PATH:", fileDir)

if __name__ == '__main__':
    print("Mapiot stands for Minecraft API organization tool")
    funcToExecute = whatToDo()
    if funcToExecute == "UUID":
        playerAPI()
    elif funcToExecute == "serverIP":
        serverAPI()
    elif funcToExecute == "slimeChecker":
        slimeChunckFinder()

