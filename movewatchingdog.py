import requests
import asyncio
import time
from mwbot import Bot

def getRedirect(pagename):
    api = f'https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=redirects&titles={pagename}&formatversion=2'
    sent = requests.get(api)
    json = sent.json()
    if "redirects" in json['query']['pages'][0]:
        getLen = len(json['query']['pages'][0]['redirects'])
        Len = list(range(getLen))
        redirects = []
        for x in Len:
            redirects.append(str(json['query']['pages'][0]['redirects'][x]["title"]))
        return redirects
    else:
        return False
    
moveapi = 'https://zh.wikipedia.org/w/api.php?action=query&format=json&list=logevents&formatversion=2&leprop=ids%7Ctitle%7Ctype%7Cdetails&letype=move'
moveSent = requests.get(moveapi)
moveJson = moveSent.json()
moveGetLen = len(moveJson['query']['logevents'])
moveLen = list(range(moveGetLen))
originalPages = []
targetPages = []
for x in moveLen:
    originalPages.append(str(moveJson['query']['logevents'][x]['title']))
    targetPages.append(str(moveJson['query']['logevents'][x]['params']['target_title']))

async def main(originalPage, redirectPages, targetPage):
    bot = Bot(
        sitename = "zh.wikipedia",
        api = "https://zh.wikipedia.org/w/api.php",
        index = "https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5",
        username = "",
        password = ""
    )
    await bot.login()
    # Get some informations so that we can avoid edit repeatly.
    
    if redirectPages != False:
        for page in redirectPages:
            for originalPage in originalPages:
                for targetPage in targetPages:
                    text = await bot.get_page_text(title=page)
                    if str(targetPage) in text:
                        return
                    else:
                        pagetext = await bot.get_page_text(title = page)
                        pagetext = pagetext.replace(originalPage, targetPage)
    else:
        pass

while True:
    asyncio.run(main())
    time.sleep(10)