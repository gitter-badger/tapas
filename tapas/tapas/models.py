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

MANAGED_COLUMNS = ['id', 'created', 'modified']

class Model(p.Model):
    class Meta:
        database = db
    
    created = p.DateTimeField()
    modified = p.DateTimeField()

    @classmethod
    def as_json(cls, data):
        return json.dumps(data, default=peewee_json)


    @classmethod
    def new_from_request(cls, data):
        item = cls()
        item.created = datetime.now()
        item.update_from_request(data)
        return item

    def update_from_request(self, data):
        fields = self._meta.fields.keys()
        fields = [f for f in fields if f not in MANAGED_COLUMNS]
        
        for f in fields:
            setattr(self, f, data[f])
        self.modified = self.created

    def update_links(self):
        pass



class Location(Model):
    link_key = 'loc'
    url_key = 'location'

    name = p.CharField()
    body = p.TextField()


class Article(Model):
    link_key = 'art'
    url_key = 'article'

    title = p.CharField()
    body = p.TextField()


class Link(Model):
    source_id = p.IntegerField()
    source_type = p.CharField()
    target_id = p.IntegerField()
    target_type = p.CharField()


def create_sample_data():
    db.connect()
    db.create_tables([Article, Location, Link])

    now = datetime.now()
    article1 = Article(
        url=str(uuid.uuid1()),
        title='title1',
        body='some longer text',
        created=now,
        modified=now
    )
    article1.save()

    db.close()

if __name__=='__main__':
    create_sample_data()
