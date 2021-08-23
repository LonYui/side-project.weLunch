from typing import Final
from flask import Flask, request
from linebot import LineBotApi
from linebot.models import TextSendMessage, template, actions
import cluster,os

app = Flask(__name__)


@app.route("/", methods=['POST'])
def webhook():
    client = LineBotApi(os.environ['lineKey'])
    rJson = request.json["events"]
    if not rJson:
        return ""
    eventType: Final = rJson[0]["type"]
    if eventType not in ["postback", "message"]:
        return
    userId: Final = rJson[0]["source"]["userId"]
    user = cluster.Member.getUser(userId)
    token: Final = rJson[0]["replyToken"]
    replyT = ""
    if eventType == "postback":
        status = user.status
        if status == 100:
            reqsT: Final = rJson[0]["postback"]["data"]
            user.status += 10
            user.save()
            date = cluster.Member.getDate(reqsT)
            date.assignValue(
                reqsT=userId, userId=userId,
                token=token, client=client)
            replyT = date.replyText(
                reqsT=userId, userId=userId,
                token=token, client=client)
            date.statusChange(reqsT=userId)
        elif status == 110:
            reqsT: Final = rJson[0]["postback"]["data"]
            date = cluster.Member.getDate(userId)
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
                    text=girl.introT(),
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
        elif reqsT in ["測試帳號男"]:
            ming = cluster.Male.objects(nickName="小明",phone="test123")[0]
            ming.userId=userId
            ming.save()
            replyT = "設置完成"
        elif reqsT in ["測試帳號女"]:
            mei = cluster.Female.objects(nickName="小美",phone="test123")[0]
            mei.userId=userId
            mei.save()
            replyT = "設置完成"
        elif reqsT == "快速使用(測試用)":
            replyT = "選擇性別"
            action1 = actions.MessageAction(text="測試帳號男", label="測試帳號男")
            action2 = actions.MessageAction(text="測試帳號女", label="測試帳號女")
            column = template.CarouselColumn(
                text=replyT, actions=[action1, action2])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId:
                client.reply_message(
                    token, [template.TemplateSendMessage(
                        template=carouse,
                        alt_text="broke")])
            return replyT
        else:
            replyT = "歡迎"
            action1 = actions.MessageAction(text="開始使用", label="開始使用")
            action2 = actions.MessageAction(text="預覽約會", label="預覽約會")
            action3 = actions.MessageAction(text="快速使用(測試用)", label="快速使用(測試用)")
            column = template.CarouselColumn(
                text=replyT, actions=[action1, action2, action3])
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
        elif reqsT == "我的交友名片" :
            replyT = "我的交友名片"
            action = actions.MessageAction(text='好',
                                           label='好')
            column = template.CarouselColumn(
                title=user.nickName, text=user.introT(),
                thumbnail_image_url=user.pictUri, actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            sendMsg = [TextSendMessage(text=replyT),
                       template.TemplateSendMessage(template=carouse,
                                                    alt_text="break")]
            if token != userId:
                client.reply_message(
                    token,sendMsg)
            return
        else:
            replyT = "歡迎"
            action = ""
            if user.isMale():
                action= actions.MessageAction(text="觀看約會", label="觀看約會")
            else:
                action= actions.MessageAction(text="發起約會", label="發起約會")
            action2 = actions.MessageAction(text="我的交友名片", label="我的交友名片")
            column = template.CarouselColumn(
                text=replyT, actions=[action,action2])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId:
                client.reply_message(
                    token, [template.TemplateSendMessage(
                        template=carouse,
                        alt_text="broke")])
            return replyT
    elif status == 110:
        date = cluster.Member.getDate(userId)
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
