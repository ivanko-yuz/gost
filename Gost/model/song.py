
import json

from datetime import datetime

from marshmallow import Schema, fields
from json import JSONEncoder

class Song:
    def __init__(self, id, title, author):
        self.song_id = id
        self.song_title = title.replace(' ', '')
        self.song_author = author.replace(' ', '')
        #self.created_at = datetime.strptime(created_at)
        #self.updated_at = datetime.strptime(updated_at)
        #datetime.datetime.now()

    def obj_dict(obj):
        return obj.__dict__

    def __repr__(self):
        return self.song_title


class SongSchema(Schema):
    song_id = fields.Int()
    song_title = fields.Str()
    song_author = fields.Str()
    ##created_at = fields.Date()
    ##updated_at = fields.Date()