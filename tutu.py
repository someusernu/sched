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


class LinkedEvent():
    def __init__(self):
        self.text = ''
        self.link = ''


class Station():
    def __init__(self):
        self.name = ''
        self.id = -1


def tutu_today():
    return datetime.datetime.now().strftime('%d.%m.%Y')


class Trip():
    def __init__(self, first, second, third, fourth, fifth, sixth, seventh, eighth, nineth):
        self.departure = self.get_departure(first)
        self.arrival = self.get_departure(second)
        self.scheduled = third.string
        self.time = fourth.string
        self.route = self.get_route(fifth)
        self.price = sixth.string
        self.actual_mov = seventh.string
        self.actual_dep = self.get_departure(eighth)
        self.actual_arr = self.get_departure(nineth)

    def get_departure(self, cell):
        departure = LinkedEvent()
        departure.text = cell.a.string
        departure.link = cell.a['href']
        return departure

    def get_route(self, cell):
        route = list()
        for point in cell.find_all('a'):
            station = Station()
            station.name = point.string
            station.id = point['href'][point['href'].find('=') + 1 :]
            route.append(station)


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
    tgs = srch.find(class_='l-etrain__main_timetable').tbody
    print(tgs.prettify())
    items = tgs.find_all_next('tr', recursive=False)
    full_sched = list()
    for i in range(len(items) - 1):
        cells = items[i].find_all_next('td', recursive=False, limit=9)
        if len(cells) == 7:
            trip = Trip(*cells, cells[0], cells[1])
        else:
            trip = Trip(*cells)
        full_sched.append(trip)
    z = 0



async def main(test=True):
    if test:
        toparse= await get_url_today(departure=41906)
    else:
        toparse = await get_url_today()
    get_roster(toparse)


if __name__ == '__main__':
    asyncio.run(main(False))
