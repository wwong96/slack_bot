from flask import Flask, request, Response, make_response
import json
from slack_sdk import WebClient
import threading
import logging
from util import *
logging.basicConfig(level=logging.INFO)


# Anonymous
with open('res/token.txt') as f:
    slack_token =  f.readline()

client = WebClient(token=slack_token)
app = Flask(__name__)

with open('command.json') as f:
    json_data = json.load(f)

command_list = json_data['command_list']


@app.route('/')
def hello_world():
    return 'Hello, World!'


def post_message(client, channel, text):
    response = client.chat_postMessage(
        channel=channel,
        text=text)
    return None


def post_image(client, channel, file, title):
    response = client.files_upload(
        channels=channel,
        file=file,
        title=title
    )
    return None


def get_answer(query, channel):
    query_list = query.split()
    recognizer = query_list[0]
    if recognizer in command_list or None:
        parser = Parser(client, channel)    
        command = command_list[recognizer]
        x = getattr(parser, command)(query_list)
        return query
    else:
        post_message(client, channel, "없는 명령어입니다. !help를 통해 명령어 목록을 확인해 주세요.\n 개발문의는 !help 개발문의를 참고해주세요 :anonymous:")
        return query


def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    if event_type == 'message':
    # if string_slack_event.find("{'type': 'message'") != -1:
        try:
            user_query = slack_event['event']['text']
            if user_query[0] != '!':
                return make_response("doesn`t start with '!'", 200, )
            get_answer(user_query[1:], channel)
            return make_response("ok", 200, )
        except IndexError:
            pass
    message = "[%s] cannot find event handler" % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

