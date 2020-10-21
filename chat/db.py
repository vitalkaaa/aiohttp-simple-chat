from aiopg import sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String
)

meta = MetaData()

users = Table(
    'users', meta,
    Column('username', String(200), nullable=False, primary_key=True),
)

messages = Table(
    'messages', meta,
    Column('id', Integer, primary_key=True),
    Column('text', String(200), nullable=False),
    Column('username',
           String(200),
           ForeignKey('users.username', ondelete='CASCADE'))
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
