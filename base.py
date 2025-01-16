import psycopg
import aiofiles
import set
import json


async def base_creds():
    file = set.BASE_CRED
    async with aiofiles.open(file, 'r', encoding='utf-8') as fil:
        base_creds = json.loads(await fil.read())
    return base_creds


async def base_connect(creation=False):
    base_cred = await base_creds()
    if creation:
        dbname = 'postgres'
    else:
        dbname = base_cred['base']
    conn = await psycopg.AsyncConnection.connect(user=base_cred['user'], password=base_cred['password'],
                                                 dbname=dbname, host=base_cred['host'], port=base_cred['port'])
    cursor = conn.cursor()
    return conn, cursor


async def create_base():
    base_cred = await base_creds()
    conn, cur = await base_connect(True)
    await cur.execute('create database %s;' % base_cred['base'])
    await conn.commit()
    await cur.execute('create user schedler;')
    await conn.commit()
    await cur.execute('grant all privileges on %s to schedler;' % base_cred['base'])
    await conn.commit()
    await cur.close()
    await conn.close()


def newbase():
    ...