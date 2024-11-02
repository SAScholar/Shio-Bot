import requests
import asyncio
import time
import re
from opencc import OpenCC
from mwbot import Bot
from config import *

stconverter = OpenCC('s2t.json')
tsconverter = OpenCC('t2s.json')
bot  = Bot(
    sitename=sitename,
    api=api,
    username=username,
    password=password
)

titles = []

def getTitles():
    queryAPI = f"https://zh.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&formatversion=2&cmtitle=Category%3A%E4%BA%8E%E5%A7%93&cmprop=ids%7Ctitle&cmlimit=500"
    querySent = requests.get(queryAPI)
    queryJson = querySent.json()
    getQueryLen = len(queryJson["query"]["categorymembers"])
    QueryLen = range(getQueryLen)
    for x in QueryLen:
        titles.append(queryJson["query"]["categorymembers"][x]["title"])

def getCharType(text):
    if stconverter.convert(text) != text:
        return "simple"
    else:
        return "traditional" 
    
async def main():
    await bot.login()
    getTitles()
    for title in titles:
        page = bot.get(title)
        if getCharType(title) == "simple":
            pattern = r"于([^()]*?)(\s*\(.*?\))?([^()]*?)"
            matches = re.findall(pattern, title)
            usingTitle = matches[0]
            trad = stconverter.convert(usingTitle)
            edit1 = "{{Noteta|zh-hans:{simple};zh-hant:{traditional;}}".format(simple=usingTitle, traditional=trad)
            edit = edit1 + page.text
            await bot.edit(title, edit, summary="Bot: 修正标题")
        else:
            pattern = r"于([^()]*?)(\s*\(.*?\))?([^()]*?)"
            matches = re.findall(pattern, title)
            usingTitle = matches[0]
            simple = stconverter.convert(usingTitle)
            edit1 = "{{Noteta|zh-hans:{simple};zh-hant:{traditional;}}".format(traditional=usingTitle, simple=simple)
            edit = edit1 + page.text
            await bot.edit(title, edit, summary="Bot: 修正标题")      
            
    print("Done!")
      