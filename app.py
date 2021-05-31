from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
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
    r = '我看不懂你在說蛇，我只知道阿修很帥'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi', 'Hi', '嗨', 'HI']:
        r = 'Hi'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是阿修的機器人'


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= r))

if __name__ == "__main__":
    app.run()