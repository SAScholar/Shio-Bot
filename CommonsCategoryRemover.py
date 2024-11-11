import requests
import asyncio
import time
import json
import re
from mwbot import Bot
from config import *

bot  = Bot(
    index = index,
    sitename=sitename,
    api=api,
    username=username,
    password=password
)

def get_category_members(category_title, api_url, limit=500):
    titles = []
    cmcontinue = None

    while True:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'categorymembers',
            'cmtitle': category_title,
            'cmlimit': limit,
        }
        if cmcontinue:
            params['cmcontinue'] = cmcontinue

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'query' in data and 'categorymembers' in data['query']:
            members = data['query']['categorymembers']
            titles.extend(member['title'] for member in members)

        if 'continue' in data:
            cmcontinue = data['continue'].get('cmcontinue')
            if not cmcontinue:
                break
        else:
            break
    
    return titles

def getPage(title):
    api = 'https://zh.wikipedia.org/w/api.php?action=parse&format=json&page={title}&prop=wikitext&formatversion=2'.format(title=title)
    sent = requests.get(api)
    json = sent.json()
    return json['parse']['wikitext']

def contains_chinese(text):
    # 定义一个包含中文字符的正则表达式
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f]')
    # 检查字符串中是否包含中文字符
    return bool(chinese_char_pattern.search(text))

async def fixCat(title):
    pagetext = getPage(title)
    pattern = r'\{\{Commons category\|([^|{}]+)}}'
    if "世界蝴蝶分類名錄" in pagetext:
        titles.remove(title)
        print(title + "包含蝶和动物界，跳过" + "剩余" + str(len(titles)) + "个页面")
    else:
        if re.search(r'\{\{Commons category\|([^|{}]+)}}', pagetext):
            pattern = r'\{\{Commons category\|([^|{}]+)}}'
            replacement = r'{{Commons category}}'
            result = re.sub(pattern, replacement, pagetext)
            await bot.edit_page(title=title,text=result,summary="按[[Wikipedia:机器人/作业请求#请求批次移除下面分类内容|作业请求]]移除Commons category模板中的参数")
            titles.remove(title)
            llen = len(titles)
            print(title + "：" + title + "Done!" + "剩余" + str(llen) + "个页面")
            time.sleep(12)
        else:
            titles.remove(title)
            print(title + "没有需要修改的Commons category模板" + "剩余" + str(len(titles)) + "个页面")

titles = get_category_members('Category:维基共享资源分类链接被定义为页面名称', 'https://zh.wikipedia.org/w/api.php')
async def main():
    await bot.login()
    for title in titles:
        await fixCat(title)

asyncio.run(main())