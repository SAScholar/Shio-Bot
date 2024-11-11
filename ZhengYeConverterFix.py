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
api = 'https://zh.wikipedia.org/w/api.php?action=query&format=json&list=search&formatversion=2&srsearch=\%22%E6%94%BF%E5%86%B6\%22&srnamespace=0&srlimit=500&srwhat=text&srsort=relevance'
data = requests.get(api).json()
length = len(data['query']['search'])

async def replacePage(page):
    pagetext = getPage(title=page)
    pagetext = pagetext.replace("政冶", "政治")
    await bot.edit_page(title=page,text=pagetext,summary="replace: 政冶 -> 政治")

def getPage(title):
    api = 'https://zh.wikipedia.org/w/api.php?action=parse&format=json&page={title}&prop=wikitext&formatversion=2'.format(title=title)
    sent = requests.get(api)
    json = sent.json()
    return json['parse']['wikitext']

for x in range(length):
    if "<span class=\"searchmatch\">政</span><span class=\"searchmatch\">冶</span>" in data['query']['search'][x]['snippet'] or "政冶" in data['query']['search'][x]['snippet']:
        titles.append(data['query']['search'][x]['title'])

async def main():
    await bot.login()
    for title in titles:
        print(title)
        if "政冶" in getPage(title=title):
            await replacePage(title)
            time.sleep(12)


asyncio.run(main())
