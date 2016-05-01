import asyncio
from multiprocessing import Process, Event
from datetime import datetime

from aiohttp import web
import tapas.models as m
import json


class DevServer():
    """Manages running a service instance in a separate process. Includes
    waiting for the service to be ready an shutting it down again. Will be
    used for testing the service, but can also be used to script the import
    of sample data into a database."""

    def __init__(self, ip='0.0.0.0', port=8089):
        self.ip = ip
        self.port = port
        self.process = None

    @property
    def root(self):
        return "http://{}:{}/".format(self.ip, self.port)

    def start(self):
        e = Event()

        def run():
            loop = asyncio.get_event_loop()
            handler = app.make_handler()
            f = loop.create_server(handler, self.ip, self.port)
            srv = loop.run_until_complete(f)
            e.set()
            try:
                loop.run_forever()
            finally:
                srv.close()
            loop.close()
        self.process = Process(target=run)
        self.process.start()
        e.wait()

    def stop(self):
        if self.process and self.process.is_alive():
            self.process.terminate()



@asyncio.coroutine
def handle(request):
    return web.Response(body="ok".encode('utf8'))


@asyncio.coroutine
def article(request):
    m.db.connect()
    data = yield from request.json()

    print(data)

    article = m.Article(
        url = data['url'],
        title = data['title'],
        body = data['body'],
        created=datetime.now()
    )
    article.save()
    m.db.close()
    return web.Response(body=m.Article.as_json(article).encode('utf-8'))




@asyncio.coroutine
def articles(request):
    m.db.connect()
    data = list(m.Article.select())
    body = m.Article.as_json(data)
    m.db.close()

    return web.Response(body=body.encode('utf-8'))


@asyncio.coroutine
def schema(request):
    m.db.connect()

    models = [m.Article]

    schema = {}

    for model in models:
        schema[model.__name__] = [f for f in model._meta.fields]
    body = json.dumps(schema)

    return web.Response(body=body.encode('utf-8'))


    m.db.close()

app = web.Application()
app.router.add_route('GET', '/', handle)
app.router.add_route('GET', '/articles', articles)
app.router.add_route('POST', '/article', article)
app.router.add_route('GET', '/schema', schema)

if __name__=='__main__':
    web.run_app(app)
