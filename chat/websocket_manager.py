import json

from chat.controllers import get_or_add_user, add_message, get_last_messages


class WebSocketManager:
    def __init__(self):
        self.websockets = {}
        self.engine = None

    async def set_db_engine(self, engine):
        self.engine = engine

    async def close(self, websocket):
        username = None
        for un, ws in self.websockets.items():
            if websocket == ws:
                username = un

        if username is not None:
            del self.websockets[username]
            await self.update_userlist()

    def get_active_users(self):
        return list(self.websockets.keys())

    def get_active_websockets(self):
        return self.websockets.values()

    async def on_login(self, ws, username):
        await get_or_add_user(self.engine, username)
        self.websockets[username] = ws
        await self.update_messagelist(ws)
        await self.update_userlist()

    async def on_message(self, username, text):
        await add_message(self.engine, username, text)
        for s in self.get_active_websockets():
            await s.send_json({'action': 'message', 'text': text, 'username': username})

    async def update_userlist(self):
        for s in self.get_active_websockets():
            await s.send_json({'action': 'userlist', 'usernames': self.get_active_users()})

    async def update_messagelist(self, ws):
        messages = await get_last_messages(self.engine)
        for msg in messages:
            await ws.send_json({'action': 'message', 'text': msg[1], 'username': msg[2]})

    async def process(self, ws):
        async for msg in ws:
            data = json.loads(msg.data)
            print(data)

            if data['action'] == 'login':
                username = data['username']
                await self.on_login(ws, username)

            if data['action'] == 'message':
                username = data['username']
                text = data['text']
                await self.on_message(username, text)

