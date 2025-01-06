import asyncio
import aiohttp
import datetime
import glbls
from bs4 import BeautifulSoup


class Event:
    def __init__(self, unusual=False, start = None, finish=None, description='', changes=''):
        self.unusual = unusual
        self.start = start
        self.finish = finish
        self.description = description
        self.changes = changes


def tutu_today():
    return datetime.datetime.now().strftime('%d.%m.%Y')


async def get_url_today(departure=43706, arrival=41406):
    async with aiohttp.ClientSession() as sess:
        rsp = await sess.get(glbls.URL_TUTU + str(departure) + '&st2=' + str(arrival) + '&date=' + tutu_today())
        txt = await rsp.read()
        return txt.decode()


def get_roster(txt):
    srch = BeautifulSoup(txt, 'html.parser')
    unusual = txt.find("Учтены изменения")
    if unusual != 1:
        unusual = True
    else:
        unusual = False
    tgs = srch.find_all(class_='l-etrain__main_timetable')
    tag = tgs[0]
    srch = tag.find_all_next('tbody', recursive=False)
    items = srch[0].find_all_next('tr', recursive=False)
    for item in items:
        print(item)
        cells = item.find_all_next('a', recursive=False)
        for cell in cells:
            print(cell)
        print('_________')


async def main(test=True):
    if test:
        toparse= await get_url_today(departure=41906)
    else:
        toparse = await get_url_today()
    get_roster(toparse)


if __name__ == '__main__':
    asyncio.run(main())
