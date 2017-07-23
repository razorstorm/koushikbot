# coding=utf-8
import json
import random

import markovify
import numpy as np

import requests
from flask import request, Flask

app = Flask(__name__)

token = 'EAAGAJhMhKRABAFbFsT55sDbAfalbtB2ZCZCbEzxZARGZBGVgARFTslOfQGTCLmIWV1zN7KbUY2qezIGmrobdbA2HkCvKo7gerksQbXhKpkhgteqCZA3R98M0XFZAwZCHdO7F2hUaRkxT9elEqF7NyqRFmaEP0g1dZA4IJsWfmX5tTwZDZD'  # noqa
ARI_TEXT_AVERAGE_LENGTH = 23


@app.route('/receive', methods=['GET'])
def serve():
    if (
        request.args.get('hub.mode') == 'subscribe' and
        request.args.get('hub.verify_token') == 'moo'
    ):
        return request.args.get('hub.challenge')
    return 'arimooster'


def generate_ari_speech():
    # Get raw text as string.
    with open("ari_parsed_text.txt") as f:
        text = f.read()

    # Build the model.
    text_model = markovify.Text(text)

    # Print five randomly-generated sentences
    num_sentences = max(1, int(round(np.random.normal(1, 0.5, 1)[0], 0)))

    sentences = []
    for i in range(num_sentences):
        sentences.append(text_model.make_short_sentence(max_chars=ARI_TEXT_AVERAGE_LENGTH*8, min_chars=ARI_TEXT_AVERAGE_LENGTH/2, tries=1000))

    sentences = " ".join(sentences)

    return sentences


@app.route('/receive', methods=['POST'])
def receive():
    print(request.data)
    data = json.loads(request.data)

    sentences = generate_ari_speech()

    try:
        for entry in data['entry']:
            for message in entry['messaging']:
                sender = message['sender']['id']
                content = message['message']['text']

                resp_msg = {
                    'recipient': {
                        'id': sender,
                    },
                    'message': {
                        'text': sentences,
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
