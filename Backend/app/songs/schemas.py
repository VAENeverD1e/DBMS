from marshmallow import Schema, fields, validate

class SongSchema(Schema):
    """Schema for a song from Jamendo"""
    jamendo_id = fields.Str(required=True)
    title = fields.Str(required=True)
    artist = fields.Str(required=True)
    album = fields.Str(allow_none=True)
    duration = fields.Int(allow_none=True)
    image_url = fields.Url(allow_none=True)
    audio_url = fields.Url(allow_none=True)
    license = fields.Str(allow_none=True)
    license_url = fields.Url(allow_none=True)
    release_date = fields.Str(allow_none=True)
    genre = fields.List(fields.Str(), allow_none=True)

class SongSearchSchema(Schema):
    """Schema for song search query"""
    query = fields.Str(required=True, validate=validate.Length(min=1))
    limit = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))
    offset = fields.Int(load_default=0, validate=validate.Range(min=0))

class GenreSearchSchema(Schema):
    """Schema for genre search"""
    genre = fields.Str(required=True, validate=validate.Length(min=1))
    limit = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))
