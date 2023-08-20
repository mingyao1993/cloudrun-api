import base64
import json


def decode_pubsub_data(pubsub_data) -> dict:
    return json.loads(base64.b64decode(pubsub_data).decode("utf-8"))
