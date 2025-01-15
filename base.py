import psycopg
import aiofiles
import set
import json


async def base_creds():
    file = set.BASE_CRED
    async with aiofiles.open(file, 'r', encoding='utf-8') as fil:
        base_creds = json.loads(await fil.read())
    return base_creds


async def base_connect():
    base_cred = await base_creds()
    conn = await psycopg.AsyncConnection.connect(user=base_cred['user'], password=base_cred['password'])
    cursor = conn.cursor()
    return conn, cursor


def newbase():
    ...