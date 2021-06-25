from typing import Final
from flask import Flask, request
from linebot import LineBotApi
from linebot.models import TextSendMessage, template, actions
import cluster

app = Flask(__name__)


@app.route("/", methods=['POST'])
def webhook():
    client = LineBotApi("jpkaZF4J41V3hTOT7kinpR16tTormHg0pKDpr5UJX6sOyeIETiHnXOYveDupNa6Zk6KKE1B+zZSiKQJ8qSrGVCeDD2EEsRzXeOEImKtQfrU1UjvLysgAvcRoGpMVos79emD+gZT3uJvF1O2pLJIQkgdB04t89/1O/w1cDnyilFU=")
    rJson = request.json["events"]
    if not rJson:
        return ""
    eventType: Final = rJson[0]["type"]
    if eventType not in ["postback", "message"]:
        return
    userId: Final = rJson[0]["source"]["userId"]
    user = cluster.getUser(userId)
    token: Final = rJson[0]["replyToken"]
    replyT = ""
    if eventType == "postback":
        status = user.status
        if status == 100:
            reqsT: Final = rJson[0]["postback"]["data"]
            user.status += 10
            user.save()
            date = cluster.getDate(reqsT)
            date.assignValue(
                reqsT=userId, userId=userId,
                token=token, client=client)
            replyT = date.replyText(
                reqsT=userId, userId=userId,
                token=token, client=client)
            date.statusChange(reqsT=userId)
        elif status == 110:
            reqsT: Final = rJson[0]["postback"]["data"]
            date = cluster.getDate(userId)
            date.assignValue(
                reqsT=reqsT, userId=userId,
                token=token, client=client)
            replyT = date.replyText(
                reqsT=reqsT, userId=userId,
                token=token, client=client)
            date.statusChange(reqsT=reqsT)
        return replyT

    # status 1 ~ 2
    reqsT: Final = rJson[0]["message"]["text"]
    if not user:
        if reqsT in ["開始使用", "去註冊約她"]:
            replyT = "請輸入性別"
            action1 = actions.MessageAction(text="男生", label="男生")
            action2 = actions.MessageAction(text="女生", label="女生")
            column = template.CarouselColumn(text=replyT,
                                             actions=[action1, action2])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId:
                client.reply_message(
                    token,
                    [template.TemplateSendMessage(template=carouse,
                                                  alt_text="broke")])
            return replyT
        elif reqsT == "預覽約會":
            replyT = "本週約會有"
            action = actions.MessageAction(text="去註冊約她", label="去註冊約她")
            columnL = []
            for girl in cluster.Female.objects(status__gte=15):
                column = template.CarouselColumn(
                    title=girl.nickName,
                    text="個性" + girl.personality
                         + "喜歡" + girl.hobit + "的"
                         + cluster.getConstellation(
                            girl.birthDate.month,
                            girl.birthDate.day) + "女孩",
                    thumbnail_image_url=girl.pictUri,
                    actions=[action])
                if len(columnL) == 10:
                    break
                else:
                    columnL.append(column)
            carouse = template.CarouselTemplate(columns=columnL)
            if token != userId:
                client.reply_message(
                    token, [TextSendMessage(text=replyT),
                            template.TemplateSendMessage(
                                template=carouse,
                                alt_text="broke")])
            return replyT
        elif reqsT in ["男生", "男"]:
            cluster.Male(userId=userId, status=3).save()
            replyT = "注意：需用<>標記訊息"
        elif reqsT in ["女生", "女"]:
            cluster.Female(status=3, userId=userId).save()
            replyT = "注意：需用<>標記訊息"
        else:
            replyT = "歡迎"
            action1 = actions.MessageAction(text="開始使用", label="開始使用")
            action2 = actions.MessageAction(text="預覽約會", label="預覽約會")
            column = template.CarouselColumn(
                text=replyT, actions=[action1, action2])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId:
                client.reply_message(
                    token, [template.TemplateSendMessage(
                        template=carouse,
                        alt_text="broke")])
            return replyT
        if token != userId:
            client.reply_message(token, TextSendMessage(text=replyT))
        return replyT
    status = user.status
    # status 3 ~ 14
    if status in range(3, 15):
        replyT = user.signup(reqsT=reqsT, client=client, token=token)

    elif status == 100:
        if reqsT == "發起約會" and not user.isMale():
            replyT = user.createDate()
        elif reqsT == "觀看約會" and user.isMale():
            user.readDate(token=token, userId=userId, client=client)
            return
        else:
            replyT = "歡迎"
            action = ""
            if user.isMale():
                action= actions.MessageAction(text="觀看約會", label="觀看約會")
            else:
                action= actions.MessageAction(text="發起約會", label="發起約會")
            column = template.CarouselColumn(
                text=replyT, actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId:
                client.reply_message(
                    token, [template.TemplateSendMessage(
                        template=carouse,
                        alt_text="broke")])
            return replyT
    elif status == 110:
        date = cluster.getDate(userId)
        if reqsT == "觀看邀請名單" and not user.isMale():
            user.readInvList(token=token, userId=userId, client=client)
            return ""
        date.assignValue(
            reqsT=reqsT, userId=userId,
            token=token, client=client)
        replyT = date.replyText(
            reqsT=reqsT, userId=userId,
            token=token, client=client)
        date.statusChange(reqsT=reqsT)
        return replyT
    if token != userId:
        client.reply_message(token, TextSendMessage(text=replyT))
    return replyT


if __name__ == '__main__':
    app.run()
