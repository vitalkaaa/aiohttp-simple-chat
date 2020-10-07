from aiopg import sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String
)

meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
)

messages = Table(
    'messages', meta,
    Column('id', Integer, primary_key=True),
    Column('text', String(200), nullable=False),
    Column('user_id',
           Integer,
           ForeignKey('users.id', ondelete='CASCADE'))
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
