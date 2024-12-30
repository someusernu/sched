import asyncio
import aiohttp
import datetime
import glbls
from bs4 import BeautifulSoup


def tutu_today():
    return datetime.datetime.now().strftime('%d.%m.%Y')


async def get_url_today():
    async with aiohttp.ClientSession() as sess:
        rsp = await sess.get(glbls.URL_TUTU + tutu_today())
        txt = await rsp.read()
        return txt.decode()


def get_roster(txt):
    srch = BeautifulSoup(txt, 'html.parser')
    tgs = srch.find_all(class_='l-etrain__main_timetable')
    tag = tgs[0]
    srch = tag.find_all_next('tbody')
    items = srch[0].find_all_next('tr')
    for item in items:
        print(item)
        cells = item.find_all_next('a')
        for cell in cells:
            print(cell)
        print('_________')


async def main():
    toparse = await get_url_today()
    get_roster(toparse)


if __name__ == '__main__':
    asyncio.run(main())
