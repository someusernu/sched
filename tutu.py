import asyncio
from multiprocessing.spawn import set_executable

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


class Trip:
    def __init__(self, cells):
        self.departure = self.get_departure(cells[0])
        self.arrival = self.get_departure(cells[1])
        self.scheduled = cells[2].string
        self.time = cells[3].string
        self.route = self.get_route(cells[4])
        self.price = cells[5].string
        if len(cells) == 9:
            self.warning = cells[6].string
            self.warninfo = self.get_departure(cells[7])
            self.actual = self.get_departure(cells[8])
        else:
            self.warning = None
            self.warninfo = self.set_none_linked_event()
            self.actual = self.set_none_linked_event()

    def __str__(self, show_route=False):
        if show_route:
            ...
        else:
            return 'Отправление - в %s, прибытие - в %s, время в пути - %s.' % (self.departure.text, self.arrival.text,
                                                                                self.time)


    def get_departure(self, cell):
        departure = LinkedEvent()
        if cell.a is not None:
            departure.text = cell.a.string
            departure.link = cell.a['href']
        else:
            departure.text = None
            departure.link = None
        return departure

    def get_route(self, cell):
        route = list()
        for point in cell.find_all('a'):
            station = Station()
            station.name = point.string
            station.id = point['href'][point['href'].find('=') + 1 :]
            route.append(station)

    def set_none_linked_event(self):
        set_none = LinkedEvent()
        set_none.text = None
        set_none.link = None
        return set_none


def check_first_row(rows):
    if rows[0].string is not None:
        return 'ушедшие' in rows[0].string
    else:
        if len(rows[0].find_all('td')) >= 6:
            return False
    return True


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
    items = tgs.find_all('tr', recursive=False)
    if check_first_row(items):
        items.pop(0)
    full_sched = list()
    for i in range(len(items) - 1):
        cells = items[i].find_all('td', recursive=False)
        if len(cells) == 9:
            trip = Trip(cells)
            full_sched.append(trip)
    for item in full_sched:
        print(item)


async def main(test=True):
    if test:
        toparse= await get_url_today(departure=41906)
    else:
        toparse = await get_url_today()
    get_roster(toparse)


if __name__ == '__main__':
    asyncio.run(main())
