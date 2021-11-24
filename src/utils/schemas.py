from datetime import datetime
from marshmallow import Schema, fields
from .constants import FLASK_ENV, MODEL_PATH, VERSION, PROJECT


# Schemas
class HealthSchema(Schema):
    project = fields.String(default='', example=PROJECT)
    version = fields.String(default='', example=VERSION)
    environment = fields.String(default='', example=FLASK_ENV)
    date = fields.String(default='', example=datetime.now())


class GetLyrics(Schema):
    lyric_input = fields.String(required=True, default='', example='Love')
    percentage = fields.Integer(required=True, default=100, example=100)


class ResponsePost(Schema):
    setup = fields.String(required=True, default='', example=MODEL_PATH)
    generated_lyric = fields.String(required=True, default='', example='Love is in the air')


class PostLyrics(Schema):
    response = fields.Nested(ResponsePost())