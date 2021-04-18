from flask import Flask
from flask import request

from linebot import LineBotApi
from linebot.models import TextSendMessage
from typing import Final
import cluster
app = Flask(__name__)

@app.route("/",methods=['POST'])
def webhook():
    client = LineBotApi("jpkaZF4J41V3hTOT7kinpR16tTormHg0pKDpr5UJX6sOyeIETiHnXOYveDupNa6Zk6KKE1B+zZSiKQJ8qSrGVCeDD2EEsRzXeOEImKtQfrU1UjvLysgAvcRoGpMVos79emD+gZT3uJvF1O2pLJIQkgdB04t89/1O/w1cDnyilFU=")
    rJson = request.json["events"]
    if not rJson:return "ok"
    userId:Final = rJson[0]["source"]["userId"]
    user:Final = cluster.getUser(userId)
    # status 1 ~ 2
    if not user:
        reqstext:Final = rJson[0]["message"]["text"]
        token:Final = rJson[0]["replyToken"]
        replytext =""
        if reqstext == "開始使用":replytext = "請輸入性別"
        elif reqstext in ["男生","男"]:
            cluster.Male(userId=userId,status=3).save()
            replytext = "注意：需用<>標記訊息"
        elif reqstext in ["女生","女"]:
            cluster.Female(status=3,userId = userId).save()
            replytext = "注意：需用<>標記訊息"
        if token!=userId:client.reply_message(token,TextSendMessage(text=replytext))
        return replytext
    # status 3 ~ 15
    return "ok"

if __name__ == '__main__':
    app.run()