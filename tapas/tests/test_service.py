import pytest
import requests
import json
import uuid


@pytest.yield_fixture
def service():
    """Test fixture to start development server in separate process.
    Has to go to conftest.py"""
    from tapas.server import DevServer
    s = DevServer()
    s.start()
    yield s
    s.stop()


def test_main(service):
    x = requests.get(service.root + "schema").json()
    print(x)

def test_create_article(service):
    data = {
        'url': str(uuid.uuid1()),
        'title': 'test_title',
        'body': 'test_body'
    }
    a = requests.post(service.root + "article", data=json.dumps(data)).json()
    print(a)
