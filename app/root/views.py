from flask import request
from . import root
import json
from collections import namedtuple
from pyicloud import PyiCloudService

intents = {
    "intents": [{
        "intent": "iCloudIntent",
        "slots": [{
            "name": "iCloudAction",
            "type": "ICLOUD_ACTION"
        }, {
            "name": "iCloudOwner",
            "type": "ICLOUD_DEVICE_OWNERS"
        }, {
            "name": "iCloudDevice",
            "type": "ICLOUD_DEVICE_TYPE"
        }]
    }]
}

# These should move to yml
slots = [
    {"ICLOUD_ACTION":
     ["find", "locate", "status"]},
    {"ICLOUD_DEVICE_TYPE":
     ["iPhone", "iPad"]},
    {"ICLOUD_DEVICE_OWNERS":
     ["Wylie's", "Camille's", "Gage's", "Chloe's", "Ariel's"]}]

utterances = [
    "iCloudIntent iCloud {iCloudAction} {iCloudOwner} {iCloudDevice}"]

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
                "name": "AxonTrust"
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


class iCloud():
    def __init__(self, uid, pwd):
        self.api = PyiCloudService(uid, pwd)

    def findId(self, owner, device_type):
        id = 0
        for device in self.api.devices:
            if owner in str(device) and device_type in str(device):
                print '*', id, device
                return id
        return -1


def iCloudAction(action, owner, device_type):
    apple = iCloud('something@icloud.com', 'password')
    print apple.api.devices
    print apple.findId(owner, device_type)
    return True


@root.route('/', methods=['POST'])
def post():
    print json.dumps(
        request.json, indent=2, sort_keys=False, separators=(',', ': '))

    ask = json2obj(json.dumps(request.json))
    if ask.request.type == 'IntentRequest':
        print "IntentRequest"
        print ask.request

        if ask.request.intent.name == 'iCloudIntent':
            print "iCloudIntent"
            # print ask.request.intent.slots.Room.value
            iCloudAction(
                ask.request.intent.slots.iCloudAction.value,
                ask.request.intent.slots.iCloudOwner.value,
                ask.request.intent.slots.iCloudDevice.value)

            if ask.request.intent.slots.iCloudAction.value == 'find':
                pre_action = "I have alerted"
                post_action = ".  I hope you find it!"
            else:
                pre_action = ask.request.intent.slots.iCloudAction.value
                post_action = ""

            return generate_response(
                "{} {} {} {}".format(
                    pre_action,
                    ask.request.intent.slots.iCloudOwner.value,
                    ask.request.intent.slots.iCloudDevice.value,
                    post_action
                )), 200, CONTENT_TYPE
        else:
            return generate_response(
                "Unknown Intent."), 200, CONTENT_TYPE
    elif ask.request.type == 'LaunchRequest':
        print "LaunchRequest"
        return generate_response("Yes?", endSession=False), 200, CONTENT_TYPE
    else:
        return generate_response(
            "Unknown request type. Not an intent."), 200, CONTENT_TYPE
