import json
from datetime import datetime
import uuid
import os.path

import peewee as p

path = os.path.split(__file__)[0]
db = p.SqliteDatabase(os.path.join(path, 'flaneur.db'))

def peewee_json(obj):
    if isinstance(obj, Model):
        keys = obj._meta.fields.keys()
        return {f: getattr(obj,f) for f in keys}
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


class Model(p.Model):
    class Meta:
        database = db

    @classmethod
    def as_json(cls, data):
        return json.dumps(data, default=peewee_json)


class Article(Model):
    url = p.CharField(unique=True)
    title = p.CharField()
    body = p.TextField()
    created = p.DateTimeField()


def create_sample_data():
    db.connect()
    db.create_tables([Article])

    article1 = Article(
        url=str(uuid.uuid1()),
        title='title1',
        body='some longer text',
        created=datetime.now()
    )
    article1.save()

    db.close()

if __name__=='__main__':
    create_sample_data()
