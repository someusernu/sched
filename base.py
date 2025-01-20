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
    creds = await base_creds()
    if creation:
        dbname = 'postgres'
        user = creds['user']
        password = creds['password']
    else:
        dbname = creds['base']
        user = creds['user_base']
        password = creds['password_base']
    conn = await psycopg.AsyncConnection.connect(user=user, password=password, dbname=dbname, host=creds['host'],
                                                 port=creds['port'])
    cursor = conn.cursor()
    return conn, cursor


async def create_base():
    creds = await base_creds()
    conn, cur = await base_connect(True)
    await conn.set_autocommit(True)
    await cur.execute('CREATE DATABASE %s;' % creds['base'])
    chk = await cur.execute('''select 1 from pg_roles where rolname = '%s';''' % creds['user'])
    chk = await chk.fetchone()
    if chk is None:
        await cur.execute('''create user %s with password '%s';''' % (creds['user_base'], creds['password_base']))
    await cur.execute('grant all privileges on database %s to %s;' % (creds['base'], creds['user_base']))
    await cur.close()
    await conn.close()


async def create_tables():
    conn, cur = await base_connect()
    chk = await cur.execute('''select * from public.tables where table_name = 'users';''')
    chk = chk.fetchall()
    print(chk)


async def drop_base():
    conn, cur = await base_connect(True)
    await conn.set_autocommit(True)
    creds = await base_creds()
    await cur.execute('drop database %s;' % creds['base'])
