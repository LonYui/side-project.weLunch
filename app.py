from flask import Flask
from flask import request
from datetime import date

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
    userId:Final = rJson[0]["source"]["userId"]
    user = cluster.getUser(userId)
    # status 1 ~ 2
    reqstext:Final = rJson[0]["message"]["text"]
    token:Final = rJson[0]["replyToken"]
    replytext =""
    if not user:
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
    status = user.status
    if status==3:
        user.status+=1
        replytext="請輸入<名字>"
    elif status==4:
        m = re.search("<(\S+)>",reqstext)
        if m:user.nickName=m.groups()[0]
        user.status+=1
        replytext="請輸入<生日> (yyyy-mm-dd)"
    elif status==5:
        # replytext="您是1995-03-25的牡羊男孩嗎？"
        m = re.search("<(\S+)>",reqstext)
        if m:user.birthDate=date.fromisoformat(m.groups()[0])
        user.status+=1
        replytext="您是"+user.birthDate.isoformat()+"的"+cluster.getConstellation(user.birthDate.month,user.birthDate.day)
        if user.__class__.__name__=="Male":replytext+="男孩嗎？"
        elif user.__class__.__name__=="Female":replytext+="女孩嗎？"
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
        if m:user.personality=m.groups()[0]
        user.status+=1
        replytext="請輸入<興趣>"
    elif status==8:
        m = re.search("<(\S+)>",reqstext)
        if m:user.hobit=m.groups()[0]
        user.status+=1
        replytext="請輸入<職業>"
    elif status==9:
        m = re.search("<(\S+)>",reqstext)
        if m:user.job=m.groups()[0]
        user.status+=1
        replytext="請輸入<照片url>"
    elif status==10:
        m = re.search("<(\S+)>",reqstext)
        if m:user.pictUri=m.groups()[0]
        user.status+=1
        replytext="請輸入<信箱>"
    elif status==11:
        m = re.search("<(\S+)>",reqstext)
        if m:user.email=m.groups()[0]
        user.status+=1
        replytext="請輸入<電話>"
    elif status==12:
        m = re.search("<(\S+)>",reqstext)
        if m:user.phone=m.groups()[0]
        user.status+=1
        replytext="請輸入驗證碼，查看手機簡訊"
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
            action = actions.MessageAction(text="沒錯",label="沒錯")
            column = template.CarouselColumn(title=user.nickName,
                                    text="個性" + user.personality + "喜歡" + user.hobit + "的女孩",
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
    user.save()
    if token!=userId:client.reply_message(token,TextSendMessage(text=replytext))
    return replytext

if __name__ == '__main__':
    app.run()