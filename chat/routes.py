from chat.views import chat, websocket_handler, login_page, login


def setup_routes(app):
    app.router.add_get('/', chat)
    app.router.add_get('/login', login_page)
    app.router.add_post('/login', login)
    app.router.add_get('/ws', websocket_handler)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path='chat/static',
                          name='static')
