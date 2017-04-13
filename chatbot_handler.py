# coding=utf-8
import json

from random import random
import requests
from flask import request, Flask

app = Flask(__name__)

token = 'EAAGAJhMhKRABAFbFsT55sDbAfalbtB2ZCZCbEzxZARGZBGVgARFTslOfQGTCLmIWV1zN7KbUY2qezIGmrobdbA2HkCvKo7gerksQbXhKpkhgteqCZA3R98M0XFZAwZCHdO7F2hUaRkxT9elEqF7NyqRFmaEP0g1dZA4IJsWfmX5tTwZDZD'  # noqa


@app.route('/receive', methods=['GET'])
def serve():
    if (
        request.args.get('hub.mode') == 'subscribe' and
        request.args.get('hub.verify_token') == 'moo'
    ):
        return request.args.get('hub.challenge')
    return 'arimooster'


koush_resps = [
    "🐮s are social animals, and they naturally form large herds. And like people, they will make friends and bond to some herd members, while avoiding others",
    "🐮s are red-green colorblind. In a bullfight, its the waving of the cape that attracts the bull not the red color",
    "A 🐮's heart beats between 60 and 70 beats per minute",
    "🐮s can hear lower and higher frequencies better than humans.",
    "An average dairy 🐮 weighs about 1,200 pounds.",
    "A 🐮s normal body temperature is 101.5°F.",
    "The average 🐮 chews at least 50 times per minute.",
    "The typical 🐮 stands up and sits down about 14 times a day.",
    "An average 🐮 has more than 40,000 jaw movements in a day.",
    "🐮s actually do not bite grass; instead they curl their tongue around it.",
    "🐮s have almost total 360-degree panoramic vision.",
    "🐮s have a single stomach, but four different digestive compartments.",
    "🐮s are pregnant for 9 months just like people",
    "A dairy 🐮 can produce 125 lbs. of saliva a day",
    "🐮s spend 8 hours per day eating, 8 hours chewing her cud (regurgitated, partially digested food), and 8 hours sleeping",
    "You can lead a 🐮 upstairs, but not downstairs. 🐮s knees can't bend properly to walk downstairs.",
    "🐮s can't vomit",
    "The average 🐮 drinks 30 to 50 gallons of water each day",
    "The average 🐮 produces 70 lbs. of milk. That's 8 gallons per day!",
    "🐮s only have teeth on the bottom",
    "🐮s have a great sense of smell. They can smell something up to 6 miles away",
    "Dairy 🐮s are economic job creating machines! 1 dairy 🐮 creates 4 full time jobs in the local community",
    "A Holstein's spots are like a fingerprint. No two 🐮s have exactly the same pattern of black and white spots. They are all different",
    "The average 🐮 will eat about 100 lbs. of feed per day",
]


@app.route('/receive', methods=['POST'])
def receive():
    print(request.data)
    data = json.loads(request.data)

    try:
        for entry in data['entry']:
            for message in entry['messaging']:
                sender = message['sender']['id']
                content = message['message']['text']
                koush_resp = koush_resps[int(random() * len(koush_resps))].format(inbound_msg=content)  # noqa

                resp_msg = {
                    'recipient': {
                        'id': sender,
                    },
                    'message': {
                        'text': koush_resp,
                    },
                }

                response = requests.post(
                    'https://graph.facebook.com/v2.6/me/messages',
                    params={'access_token': token},
                    json=resp_msg,
                )
                print('Sent requests %s' % json.dumps(resp_msg))
                print('Received response %s' % response.text)
    except Exception as e:
        print(e)
        return 'not handled'

    return 'success'
