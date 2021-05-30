from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('rSx+6h0uPBQmUbjzPYLtmSv4KBedcCq69v8zBakhq00DrvsuEGqiwcoNbmkrdhUi78WJURt/hKKBHricj0IOznfL4ue/pQjua/+bFztZsJWiU3QG3ZMxFtjDiLQiqIYcFb7BueRQTgJ/AzG2iU3nCwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f8bd045fbfb53225f78d0aecfe6153d7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    s = '阿修很帥'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= s))

if __name__ == "__main__":
    app.run()