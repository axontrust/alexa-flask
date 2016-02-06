import json
from collections import namedtuple
from flask import request
from app import app

CONTENT_TYPE = {'Content-Type': 'application/json;charset=UTF-8'}


def generate_response(output_speech,
                      card_title="",
                      card_subtitle="",
                      card_content="",
                      session_attributes={},
                      endSession=True):
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "user": {
                "name": "nelson"
            }
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "card": {
                "type": "Simple",
                "title": card_title,
                "subtitle": card_subtitle,
                "content": card_content
            },
            "shouldEndSession": endSession
        }
    }
    return json.dumps(response)


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())


def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


@app.route('/', methods=['POST'])
def post():
    print json.dumps(
        request.json, indent=2, sort_keys=False, separators=(',', ': '))

    ask = json2obj(json.dumps(request.json))
    if ask.request.type == 'IntentRequest':
        print "IntentRequest"
        print ask.request
        if ask.request.intent.name == 'HelloIntent':
            print "HelloIntent"
            print ask.request.intent.slots.Room.value
            return generate_response(
                "{}".format(
                    ask.request.intent.slots.Room.value)), 200, CONTENT_TYPE
        else:
            return generate_response(
                "Unknown Intent."), 200, CONTENT_TYPE
    elif ask.request.type == 'LaunchRequest':
        print "LaunchRequest"
        return generate_response("Yes?", endSession=False), 200, CONTENT_TYPE
    else:
        return generate_response(
            "Unknown request type. Not an intent."), 200, CONTENT_TYPE
