# -*- coding: utf-8 -*-
import sys
import json
from flask import Flask, request
import telepot
import requests


try:
    from Queue import Queue
except ImportError:
    from queue import Queue

"""
$ python2.7 webhook_flask_skeleton.py <token> <listening_port> <webhook_url>
Webhook path is '/abc' (see below), therefore:
<webhook_url>: https://<base>/abc
"""

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if msg.get('text').encode('utf-8') == 'погода':
        weather = requests.get('http://api.openweathermap.org/data/2.5/find?q=Dnipropetrovsk&units=metric&appid=690371b58dcfba32ca9826b8e7bb3fe7')
        if weather:
            now = weather.json()['list'][0]['main']['temp']
            bot.sendMessage(chat_id, 'Погода зараз: {}°'.format(now))
    print 'Normal Message:', content_type, chat_type, chat_id

# need `/setinline`
def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print 'Inline Query:', query_id, from_id, query_string

    # Compose your own answers
    articles = [{'type': 'article',
                    'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

    bot.answerInlineQuery(query_id, articles)

# need `/setinlinefeedback`
def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print 'Chosen Inline Result:', result_id, from_id, query_string





TOKEN = '' #telegram token
# 443, 80, 88, 8443,
PORT = 8443
URL = '' #heroku app url wbhook

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.notifyOnMessage({'normal': on_chat_message,
                     'inline_query': on_inline_query,
                     'chosen_inline_result': on_chosen_inline_result}, source=update_queue)  # take updates from queue

@app.route('/abc', methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(port=PORT, debug=True)