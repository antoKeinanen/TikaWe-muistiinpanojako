import flask
import json


def inject_fields() -> dict:
    fields = flask.get_flashed_messages(category_filter="fields")
    if fields:
        return {"fields": json.loads(fields[0])}
    return {}
