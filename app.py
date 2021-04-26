from flask import Flask
from flask import request
from datetime import date as dt

from linebot import LineBotApi
from linebot.models import TextSendMessage,template,actions
from typing import Final
import cluster,re

app = Flask(__name__)

@app.route("/",methods=['POST'])
def webhook():
    client = LineBotApi("jpkaZF4J41V3hTOT7kinpR16tTormHg0pKDpr5UJX6sOyeIETiHnXOYveDupNa6Zk6KKE1B+zZSiKQJ8qSrGVCeDD2EEsRzXeOEImKtQfrU1UjvLysgAvcRoGpMVos79emD+gZT3uJvF1O2pLJIQkgdB04t89/1O/w1cDnyilFU=")
    rJson = request.json["events"]
    if not rJson:return "ok"
    Etype:Final = rJson[0]["type"]
    if Etype not in ["postback","message"]:return
    userId:Final = rJson[0]["source"]["userId"]
    user = cluster.getUser(userId)
    token:Final = rJson[0]["replyToken"]
    replytext =""
    if Etype == "postback":
        status = user.status
        if status==100:
            reqstext:Final = rJson[0]["postback"]["data"]
            user.status+=10
            date = cluster.getDate(reqstext)
            replytext = date.ST_Dstatus(reqstext=userId,userId=userId,token=token,client=client)
            user.save()
            return replytext
        elif status==110:
            reqstext:Final = rJson[0]["postback"]["data"]
            date = cluster.getDate(userId)
            replytext = date.ST_Dstatus(reqstext=reqstext,userId=userId,token=token,client=client)
            return replytext

    # status 1 ~ 2
    reqstext:Final = rJson[0]["message"]["text"]
    if not user:
        if reqstext in ["開始使用","去註冊約她"]:
            replytext = "請輸入性別"
            action1 = actions.MessageAction(text="男生", label="男生")
            action2 = actions.MessageAction(text="女生", label="女生")
            column = template.CarouselColumn(text=replytext, actions=[action1, action2])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
            return replytext
        elif reqstext=="預覽約會":
            replytext = "本週約會有"
            action = actions.MessageAction(text="去註冊約她", label="去註冊約她")
            columnL=[]
            for girl in cluster.Female.objects(status__gte=15):
                column = template.CarouselColumn(title=girl.nickName,
                                                 text="個性" + girl.personality + "喜歡" + girl.hobit + "的"+cluster.getConstellation(girl.birthDate.month,girl.birthDate.day)+"女孩",
                                                 thumbnail_image_url=girl.pictUri,
                                                 actions=[action])
                if len(columnL) ==10:break
                else :columnL.append(column)
            carouse = template.CarouselTemplate(columns=columnL)
            if token != userId: client.reply_message(token, [TextSendMessage(text=replytext),template.TemplateSendMessage(template=carouse,alt_text="broke")])
            return replytext
        elif reqstext in ["男生","男"]:
            cluster.Male(userId=userId,status=3).save()
            replytext = "注意：需用<>標記訊息"
        elif reqstext in ["女生","女"]:
            cluster.Female(status=3,userId = userId).save()
            replytext = "注意：需用<>標記訊息"
        else:
            replytext= "歡迎"
            action1 = actions.MessageAction(text="開始使用", label="開始使用")
            action2 = actions.MessageAction(text="預覽約會", label="預覽約會")
            column = template.CarouselColumn(text=replytext,actions=[action1,action2])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
            return replytext
        if token!=userId:client.reply_message(token,TextSendMessage(text=replytext))
        return replytext
    status = user.status
    # status 3 ~ 15
    if status==3:
        user.status+=1
        replytext="請輸入<名字>"
    elif status==4:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.nickName=m.groups()[0]
        user.status+=1
        replytext="請輸入<生日> (yyyy-mm-dd)"
    elif status==5:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.birthDate=dt.fromisoformat(m.groups()[0])
        user.status+=1
        replytext="您是"+user.birthDate.isoformat()+"的"+cluster.getConstellation(user.birthDate.month,user.birthDate.day)
        if user.__class__.__name__=="Male":replytext+="男孩嗎？"
        elif user.__class__.__name__=="Female":replytext+="女孩嗎？"
        action1 = actions.MessageAction(text="沒錯", label="沒錯")
        action2 = actions.MessageAction(text="剛剛手滑了", label="剛剛手滑了")
        column = template.CarouselColumn(text=replytext, actions=[action1, action2])
        carouse = template.CarouselTemplate(columns=[column])
        if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                      alt_text="broke")])
        user.save()
        return replytext

    elif status==6:
        if reqstext in ["是","沒錯","y"]:
            user.status+=1
            replytext="請輸入<個人特質>"
        elif reqstext in ["不是","剛剛手滑了","n"]:
            user.status-=1
            user.birthDate = None
            replytext="請輸入<生日> (yyyy-mm-dd)"
    elif status==7:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.personality=m.groups()[0]
        user.status+=1
        replytext="請輸入<興趣>"
    elif status==8:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.hobit=m.groups()[0]
        user.status+=1
        replytext="請輸入<職業>"
    elif status==9:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.job=m.groups()[0]
        user.status+=1
        replytext="請輸入<照片url>"
    elif status==10:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.pictUri=m.groups()[0]
        user.status+=1
        replytext="請輸入<信箱>"
    elif status==11:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.email=m.groups()[0]
        user.status+=1
        replytext="請輸入<電話>"
    elif status==12:
        m = re.search("<(\S+)>",reqstext)
        if not m:
            if token !=userId:client.reply_message(token,TextSendMessage(text="偵測不到<>，請再試一次"))
            return "偵測不到<>，請再試一次"
        user.phone=m.groups()[0]
        user.status+=1
        replytext="請輸入<驗證碼>，查看手機簡訊"
    elif status==13:
        m = re.search("<(\S+)>",reqstext)
        validatCode = m.groups()[0]
        if validatCode!="iampassword":
            user.phone=None
            user.status-=1
            replytext="錯誤，請再輸入一次手機"
        else:
            user.status+=1
            replytext="最後確認，這樣資料正確嗎？"
            text = "個性" + user.personality + "喜歡" + user.hobit + "的"+\
                   cluster.getConstellation(user.birthDate.month,user.birthDate.day)+"男孩"
            if user.__class__.__name__ == "Male":
                text += "男孩"
            elif user.__class__.__name__ == "Female":
                text += "女孩"
            action = actions.MessageAction(text="沒錯",label="沒錯")
            column = template.CarouselColumn(title=user.nickName,
                                    text=text,
                                    thumbnail_image_url=user.pictUri,
                                    actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            if token!=userId:
                client.reply_message(token, [TextSendMessage(text=replytext),template.TemplateSendMessage(template=carouse,alt_text="broke")])
            user.save()
            return replytext
    elif status==14:
        if reqstext in ["是","沒錯","y","確認"]:
            user.status+=1
            replytext="待審核後就可以開始使用了"

    elif status==100:
        if reqstext=="發起約會":
            replytext = "上班在哪一區呀？"
            cluster.Date(femaleId=user.userId,status=1).save()
            user.status+=10
        elif reqstext=="觀看約會":
            colLis = []
            for dating in cluster.Date.objects(status==10):
                girl = cluster.getUser(dating.femaleId)
                action = actions.PostbackAction(data=dating.femaleId,label="邀請她",display_text="邀請她")
                column = template.CarouselColumn(actions=[action],
                                                 title = str( cluster.calculate_age(girl.birthDate) )+","+girl.nickName,
                                                 text = "我在"+dating.workDist+"上班，喜歡"+dating.eatype+"，拜"+str(dating.dateDate.isoweekday() )+"有空嗎？",
                                                 thumbnail_image_url = girl.pictUri,
                                                 )
                colLis.append(column)
            carouse = template.CarouselTemplate(columns=colLis)
            if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
            return replytext
    elif status==110:
        date = cluster.getDate(userId)
        if reqstext=="觀看邀請名單":
            colLis = []
            for id in date.invList:
                user = cluster.getUser(id)
                text = "個性" + user.personality + "喜歡" + user.hobit + "的" + \
                       cluster.getConstellation(user.birthDate.month, user.birthDate.day) + "男孩"
                if user.__class__.__name__ == "Male":
                    text += "男孩"
                elif user.__class__.__name__ == "Female":
                    text += "女孩"
                action = actions.PostbackAction(data=id,label="選他",display_text="選他")
                column = template.CarouselColumn(title=user.nickName,
                                                 text=text,
                                                 thumbnail_image_url=user.pictUri,
                                                 actions=[action])
                colLis.append(column)
            carouse = template.CarouselTemplate(columns=colLis)
            if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
            return ""
        replytext = date.ST_Dstatus(reqstext=reqstext,userId=userId,token=token,client=client)
        return replytext
    user.save()
    if token!=userId:client.reply_message(token,TextSendMessage(text=replytext))
    return replytext

if __name__ == '__main__':
    app.run()