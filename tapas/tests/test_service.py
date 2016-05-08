import pytest
import requests
import json
import uuid
import os, os.path

import tapas.models as m

here = os.path.split(__file__)[0]
sample_db = os.path.join(here, "sample.db")


@pytest.yield_fixture
def service():
    """Test fixture to start development server in separate process.
    Has to go to conftest.py"""
    from tapas.server import DevServer
    s = DevServer(sample_db, init_tables=True)
    s.start()
    yield s
    s.stop()
    os.remove(sample_db)


def test_main(service):
    x = requests.get(service.root + "schema").json()
    print(x)

def test_create_article(service):
    data = {
        'title': 'test_title',
        'body': 'test_body'
    }
    a = requests.post(service.root + "article", data=json.dumps(data)).json()
    print(a)

def test_create_location(service):
    data = {
        'name': 'test_name',
        'body': 'test_body'
    }
    a = requests.post(service.root + "location", data=json.dumps(data)).json()
    print(a)
