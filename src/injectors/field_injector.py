import flask
import json


def inject_fields() -> dict:
    """
    Retrieve flashed field data from the Flask session and prepare them for
    injection into templates.

    This function collects field data that have been flashed with the category
    `"fields"`. If field data is found, it is parsed from JSON format and returned
    in a dictionary.

    The action called by the form should be decorated with `@flash_fields` decorator.

    Returned value is automatically injected for usage in jinja templates.

    Returns:
        dict: A dictionary containing the parsed field data. If no field data is
        found, an empty dictionary is returned.
    """

    fields = flask.get_flashed_messages(category_filter="fields")
    if fields:
        return {"fields": json.loads(fields[0])}
    return {}
