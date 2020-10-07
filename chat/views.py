import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session


@aiohttp_jinja2.template('index.html')
async def chat(request):
    session = await get_session(request)
    username = session.get('username')
    if username is None:
        raise web.HTTPFound('/login')

    return {'username': username}


@aiohttp_jinja2.template('login.html')
async def login_page(request):
    pass


async def login(request):
    session = await get_session(request)
    data = await request.post()
    session['username'] = data['login']
    raise web.HTTPFound('/')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    websocket_manager = request.app['wsmanager']
    await websocket_manager.process(ws)
    await websocket_manager.close(ws)

    return ws
