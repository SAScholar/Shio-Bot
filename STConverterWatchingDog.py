import requests
import asyncio
import time
import re
from opencc import OpenCC
from mwbot import Bot

stconverter = OpenCC('s2t.json')
tsconverter = OpenCC('t2s.json')

queryAPI = 'https://zh.wikipedia.org/w/api.php?action=query&format=json&list=recentchanges&formatversion=2&rctag=mw-changed-redirect-target&rcprop=title%7Ctimestamp%7Cloginfo%7Cids'
querySent = requests.get(queryAPI)
queryJson = querySent.json()
getQueryLen = len(queryJson["query"]["recentchanges"])
QueryLen = range(getQueryLen)
revids = []
title = []
edited = []

for x in QueryLen:
    revids.append(queryJson["query"]["recentchanges"][x]["revid"])
    title.append(queryJson["query"]["recentchanges"][x]["title"])

def getRevText(revid) -> str:
    api = f'https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&revids={revid}&formatversion=2&rvprop=ids%7Ccontent'
    sent = requests.get(api)
    json = sent.json()
    text = json['query']['pages'][0]['revisions'][0]['content']
    pattern = r'#(?:REDIRECT|redirect|重定向|重新導向)\s*\[\[(.*?)\]\]'
    matches = re.findall(pattern, text)
    return matches[0]

def available(page) -> bool:
    api = f'https://zh.wikipedia.org/w/api.php?action=query&format=json&titles={page}&formatversion=2'
    sent = requests.get(api)
    json = sent.json()
    if "missing" in json["query"]["pages"][0]:
        return False
    else:
        return True

def getCharType(text):
    if stconverter.convert(text) != text:
        return "simple"
    else:
        return "traditional" 

async def main():
    bot = Bot(
        sitename = "zh.wikipedia",
        api = "https://zh.wikipedia.org/w/api.php",
        index = "https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5",
        username = "",
        password = ""
    )
    await bot.login()

    for page in title:
        page = str(page)
        if getCharType(page) == "simple":
            page = stconverter.convert(page)
        else:
            page = tsconverter.convert(page)

        print(page)
        
        for revid in revids:
            target = getRevText(revid)
            if available(page):
                atext = await bot.get_page_text(title=page)
                if str(target) in atext:
                    return
                else:
                    if page in edited:
                        continue
                    else:
                        editext = "#重定向 [[{target}]]".format(target = target)
                        await bot.edit_page(title=page,text=editext,summary="Bot: 修复重定向-任务码01")
                        edited.append(page)
            else:
                return
 
while True:
    asyncio.run(main())
    time.sleep(10)


