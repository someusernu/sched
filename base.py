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
        user = base_cred['user']
        password = base_cred['password']
    else:
        dbname = base_cred['base']
        user = base_cred['user_base']
        password = base_cred['password_base']
    conn = await psycopg.AsyncConnection.connect(user=user, password=password, dbname=dbname, host=base_cred['host'],
                                                 port=base_cred['port'])
    cursor = conn.cursor()
    return conn, cursor


async def create_base():
    base_cred = await base_creds()
    conn, cur = await base_connect(True)
    await cur.execute('create database %s;' % base_cred['base'])
    await conn.commit()
    await cur.execute("create user %s with password '%s';" % (base_cred['user_base'], base_cred['password_base']))
    await conn.commit()
    await cur.execute('grant all privileges on %s to %s;' % (base_cred['base'], base_cred['user_base']))
    await conn.commit()
    await cur.close()
    await conn.close()


async def create_tables():
    conn, cur = await base_connect()
