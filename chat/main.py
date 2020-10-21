import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from chat.db import init_pg, close_pg
from chat.routes import setup_routes, setup_static_routes
from chat.websocket_manager import WebSocketManager
from settings import config

app = web.Application()
app['config'] = config
setup_routes(app)
setup_static_routes(app)
app.on_startup.append(init_pg)
app.on_shutdown.append(close_pg)
app['wsmanager'] = WebSocketManager()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('chat/templates'))

setup(app, EncryptedCookieStorage(b'12345678901234567890123456789012'))

web.run_app(app)
