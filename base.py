import psycopg
import aiofiles
import set
import json


async def base_creds():
    file = set.BASE_CRED
    async with aiofiles.open(file, 'r', encoding='utf-8') as fil:
        base_creds = json.loads(await fil.read())
    return base_creds


async def base_connect(creation=False, admin=False):
    creds = await base_creds()
    if creation:
        dbname = 'postgres'
        user = creds['user']
        password = creds['password']
    else:
        dbname = creds['base']
        user = creds['user_base']
        password = creds['password_base']
    if admin:
        user = 'postgres'
        password = creds['password']
    conn = await psycopg.AsyncConnection.connect(user=user, password=password, dbname=dbname, host=creds['host'],
                                                 port=creds['port'])
    cursor = conn.cursor()
    return conn, cursor


async def create_base():
    creds = await base_creds()
    conn, cur = await base_connect(True)
    await conn.set_autocommit(True)
    await cur.execute('''CREATE DATABASE "%s";''' % creds['base'])
    chk = await cur.execute('''SELECT 1 FROM pg_roles WHERE rolname = '%s';''' % creds['user'])
    chk = await chk.fetchone()
    if chk is None:
        await cur.execute('''CREATE USER %s WITH PASSWORD '%s';''' % (creds['user_base'], creds['password_base']))
    await cur.execute('''ALTER DATABASE "%s" OWNER TO %s;''' % (creds['base'], creds['user_base']))
    await cur.execute('GRANT ALL PRIVILEGES ON DATABASE "%s" to %s;' % (creds['base'], creds['user_base']))
    await cur.close()
    await conn.close()
    conn, cur = await base_connect(admin=True)
    await cur.execute('GRANT ALL ON schema public to %s;' % creds['user_base'])
    await cur.close()
    await conn.close()



async def create_tables():
    conn, cur = await base_connect()
    chk = await cur.execute('''SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users';''')
    chk = await chk.fetchall()
    if len(chk) == 0:
        await cur.execute('''CREATE table users (
            uid SERIAL PRIMARY KEY,
            uname character varying(25),
            mail character varying(100),
            password character varying(100)
        );''')
        await conn.commit()
        await cur.execute('''create table events (
            eid serial primary key,
            owner integer,
            text character varying,
            created date,
            manual date,
            previous boolean,
            before_previous boolean,
            manual_result boolean,
            previous_result boolean,
            before_previous_result boolean,
            type_tel boolean,
            type_mail boolean,
            type_app boolean,
            foreign key (owner) references users(uid)
        );''')
        await conn.commit()
        await conn.close()


async def drop_base():
    conn, cur = await base_connect(True)
    await conn.set_autocommit(True)
    creds = await base_creds()
    await cur.execute('DROP DATABASE "%s";' % creds['base'])
