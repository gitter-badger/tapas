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
def status(request):
    return web.Response(body="Service is up and running ...".encode('utf8'))


def register_entity(router, entity):
    
    @asyncio.coroutine
    def create(request):
        m.db.connect()
        data = yield from request.json()
        item = entity.new_from_request(data)
        item.save()
        m.db.close()
        return web.Response(body=entity.as_json(item).encode('utf-8'))
    
    app.router.add_route('POST', '/{}'.format(entity.url_key), create)


    @asyncio.coroutine
    def read(request):
        m.db.connect()
        data = list(entity.select())
        body = entity.as_json(data)
        m.db.close()
        return web.Response(body=body.encode('utf-8'))
    
    app.router.add_route('GET', '/{}s'.format(entity.url_key), read)




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
app.router.add_route('GET', '/', status)
app.router.add_route('GET', '/schema', schema)
register_entity(app.router, m.Article)
register_entity(app.router, m.Location)

if __name__=='__main__':
    web.run_app(app)
