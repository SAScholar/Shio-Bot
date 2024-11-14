import requests
import asyncio
import time
import json
from mwbot import Bot
from config import *

bot  = Bot(
    index = index,
    sitename=sitename,
    api=api,
    username=username,
    password=password
)

titles = []
api = 'https://zh.wikipedia.org/w/api.php?action=query&format=json&list=search&formatversion=2&srsearch="{titlesn}"%22"&srnamespace=0&srlimit=500&srwhat=text&srsort=relevance'.format(titlesn="山西全国重点文物保护单位")
data = requests.get(api).json()
length = len(data['query']['search'])

async def replacePage(page):
    pagetext = getPage(title=page)
    pagetext = pagetext.replace("山西全国重点文物保护单位", "山西省境内的全国重点文物保护单位")
    await bot.edit_page(title=page,text=pagetext,summary="replace: 山西全国重点文物保护单位 -> 山西省境内的全国重点文物保护单位 [[WikiProject_talk:中国文化遗产#关于文物保护单位分类_2|已有共识]]&[[Wikipedia:机器人/作业请求#请求更改涉及全国重点文物保护单位的内容|作业请求]]")

def getPage(title):
    api = 'https://zh.wikipedia.org/w/api.php?action=parse&format=json&page={title}&prop=wikitext&formatversion=2'.format(title=title)
    sent = requests.get(api)
    json = sent.json()
    return json['parse']['wikitext']

for x in range(length):
    titles.append(data['query']['search'][x]['title'])

async def main():
    await bot.login()
    for title in titles:
        alen = titles.index(title)
        llen = len(titles) - alen
        print(llen)
        if "各级文物保护单位列表" in title:
            continue
        else:    
            if "山西全国重点文物保护单位" in getPage(title=title):
                await replacePage(title)
                alen = titles.index(title)
                llen = len(titles) - alen
                print(title + "已处理，剩余" + str(llen) + "个页面")
                time.sleep(8)


asyncio.run(main())
