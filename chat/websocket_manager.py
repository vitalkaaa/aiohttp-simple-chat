import json


class WebSocketManager:
    def __init__(self):
        self.websockets = {}

    async def add_user(self, username, websocket):
        self.websockets[username] = websocket

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
        await self.add_user(username, ws)
        await self.update_userlist()

    async def on_message(self, username, text):
        for s in self.get_active_websockets():
            await s.send_json({'action': 'message', 'text': text, 'username': username})

    async def update_userlist(self):
        for s in self.get_active_websockets():
            await s.send_json({'action': 'userlist', 'usernames': self.get_active_users()})

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

