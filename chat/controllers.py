from chat import db


async def get_user_by_username(engine, username):
    async with engine.acquire() as conn:
        query = db.users.select().where(db.users.c.username == username)
        cursor = await conn.execute(query)
        return await cursor.fetchone()


async def add_user(engine, username):
    async with engine.acquire() as conn:
        await conn.execute(db.users.insert().values(username=username))
        return username


async def get_or_add_user(engine, username):
    user = await get_user_by_username(engine, username)
    if user is None:
        user = await add_user(engine, username)

    return user


async def add_message(engine, username, text):
    async with engine.acquire() as conn:
        query = db.messages.insert().values(username=username, text=text)
        await conn.execute(query)


async def get_last_messages(engine, limit=10):
    async with engine.acquire() as conn:
        query = db.messages.select().limit(limit)
        cursor = await conn.execute(query)
        return await cursor.fetchall()
