from sqlalchemy import create_engine, MetaData

from chat.db import users, messages
from settings import config

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[users, messages])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(users.insert(), [
        {'name': 'testuser'}
    ])

    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
