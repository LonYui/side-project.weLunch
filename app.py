from flask import Flask
from flask_mongoengine import MongoEngine
from flask import request

from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "host":"mongodb+srv://Tsung:d39105648@cluster0.dmjou.mongodb.net/Cluster0?retryWrites=true&w=majority"
}
db = MongoEngine(app)

import mongoengine as me

@app.route("/webhook",methods=['POST'])
def webhook():
    client = LineBotApi("jpkaZF4J41V3hTOT7kinpR16tTormHg0pKDpr5UJX6sOyeIETiHnXOYveDupNa6Zk6KKE1B+zZSiKQJ8qSrGVCeDD2EEsRzXeOEImKtQfrU1UjvLysgAvcRoGpMVos79emD+gZT3uJvF1O2pLJIQkgdB04t89/1O/w1cDnyilFU=")
    rJson = request.json
    for event in rJson["events"]:
        client.reply_message(event["replyToken"],TextSendMessage(text=event["message"]["text"]))
    return "ok"


if __name__ == '__main__':
    app.run()
