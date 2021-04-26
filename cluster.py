import mongoengine as me,re
from mongoengine import connect
from datetime import  date as DT,timedelta
from linebot.models import actions,template,TextSendMessage

connect(host ="mongodb+srv://Tsung:d39105648@restaurant.m9bx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" )

class Male(me.Document):
    nickName = me.StringField()
    birthDate = me.DateField()
    personality = me.StringField()
    hobit = me.StringField(max_length=20)
    job = me.StringField()
    pictUri = me.URLField()
    email = me.StringField()
    phone = me.StringField()

    userId = me.StringField(unique=True)
    status = me.IntField()
    meta = {'collection': 'Male'}

class Female(me.Document):
    nickName = me.StringField()
    birthDate = me.DateField()
    personality = me.StringField()
    hobit = me.StringField(max_length=20)
    job = me.StringField()
    pictUri = me.URLField()
    email = me.StringField()
    phone = me.StringField()

    userId = me.StringField(unique=True)
    status = me.IntField()
    meta = {'collection': 'Female'}

def getUser(userId):
    qMale = Male.objects(userId = userId)
    qFemale = Female.objects(userId = userId)
    if qMale:
        return Male.objects.get(userId =userId)
    elif qFemale:
        return Female.objects.get(userId =userId)
    else :
        return None

def getConstellation(month, date):
    """copy from https://loserfer.blogspot.com/2017/07/python_4.html"""
    dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
    constellations = ("摩羯座", "水瓶座", "雙魚座", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蝎座", "射手座", "魔羯座")
    if date < dates[month-1]:
        return constellations[month-1]
    else:
        return constellations[month]

def calculate_age(born):
    """ from stackoverflow 12 讚"""
    today = DT.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class Date(me.Document):
    workDist = me.StringField()
    lunchBreakT = me.StringField()
    lunchBreakL = me.StringField()
    eatype = me.StringField()
    dateDate = me.DateField()
    invList = me.ListField(me.StringField())
    # status 11
    inlineRes = me.StringField()

    maleId = me.StringField()
    femaleId = me.StringField(unique=True)
    status = me.IntField()
    meta = {'collection': 'Date'}

    def ST_Dstatus(self, reqstext, userId, token, client):
        tup = ((),
               ("workDist", "幾點開始午休呢", ("十二點", "十二點半", "一點")),
               ("lunchBreakT", "午休時間很長嗎？", ("普通，一小", "還行，一小半", "很長，兩小")),
               ("lunchBreakL", "喜歡吃韓式還是日式", ("日式", "韓式", "港式")),
               ("eatype", "那約個明天、後天", ("明天", "後天", "大後天")),
               ("dateDate", "成功發起約會"),(),(),(),(),
               # index:10
               ("invList","成功邀約，對象會在24小時內回覆"),
               ("maleId","開放 12hr 聊天",("討論好餐廳和時間了",)),(),(),(),(),(),(),(),(),
                # index:20
               (None,"請輸入<inLIne定位資訊>",),
               ("inlineRes","關閉聊天，約會前12hr會開啟"),(),(),(),(),(),(),(),(),
               (None,None), (), (), (), (), (), (), (), (), (),
               # index:40
               (None,"祝您約會順利")

               )
        STAT  = self.status

        # 處理assign Value
        if  STAT== 3:
            reqstext = reqstext[3:]
        elif STAT == 5:
            if reqstext == "明天":
                reqstext = DT.today() + timedelta(days=1)
            elif reqstext == "後天":
                reqstext = DT.today() + timedelta(days=2)
            elif reqstext == "大後天":
                reqstext = DT.today() + timedelta(days=3)
        elif STAT in (10,11) and getUser(reqstext) is None:
            reqstext = None
        elif STAT ==30:
            reqstext = None
        elif STAT ==21:
            m = re.search("<(\S+)>", reqstext)
            if not m:
                if token != userId: client.reply_message(token, TextSendMessage(text="偵測不到<>，請再試一次"))
                return "偵測不到<>，請再試一次"
            reqstext = m.groups()[0]
        else:pass
        attr = tup[STAT][0]
        if attr is None or reqstext is None:pass
        elif attr == 'invList':
            self[attr].append(reqstext)
        elif attr == 'maleId':
            self.invList.remove(reqstext)
            setattr(self, attr, reqstext)
        else:
            setattr(self, attr, reqstext)

        # 處理 status 變換
        if STAT in (1,2,3,4):self.status += 1
        elif STAT == 5:self.status = 10
        elif STAT == 10 and getUser(reqstext) is not None:self.status += 1
        elif STAT == 11 and  getUser(reqstext) is not None:self.status = 20
        elif STAT == 20 and reqstext == "討論好餐廳和時間了":self.status += 1
        elif STAT == 21:self.status = 30
        elif STAT == 40 and reqstext == "我出發了":
            self.status = 50
            boy = getUser(self.maleId)
            girl = getUser(self.femaleId)
            boy.status = 100
            girl.status = 100
            boy.save()
            girl.save()
        else:pass
        # 處理 replyMessage
        replytext = tup[STAT][1]
        if STAT in (1, 2, 3, 4):
            action1 = actions.MessageAction(text=tup[STAT][2][0], label=tup[STAT][2][0])
            action2 = actions.MessageAction(text=tup[STAT][2][1], label=tup[STAT][2][1])
            action3 = actions.MessageAction(text=tup[STAT][2][2], label=tup[STAT][2][2])
            column = template.CarouselColumn(text=replytext, actions=[action1, action2, action3])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
        elif STAT in(10,) and getUser(reqstext) is None:
            replytext = "無人邀請"
        elif STAT in (11,) and getUser(reqstext) is None:
            replytext = "有人邀約了"
            action = actions.MessageAction(text="觀看邀請名單", label="觀看邀請名單")
            column = template.CarouselColumn(text=replytext, actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
            return replytext
        elif STAT in (11,):
            action = actions.MessageAction(text=tup[STAT][2][0], label=tup[STAT][2][0])
            column = template.CarouselColumn(text=replytext, actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, TextSendMessage(text=replytext))
            if token != userId: client.push_message(self.maleId, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
        elif STAT in (20,40) and reqstext not in ("討論好餐廳和時間了","我出發了"):
            to,prefix =("","")
            if userId==self.maleId:
                to=self.femaleId
                prefix = "👦:"
            else:
                to=self.maleId
                prefix = "👩:"
            if token != userId: client.push_message(to,TextSendMessage(text=prefix+reqstext))
            return reqstext
        elif STAT ==20:
            to, prefix = ("", "")
            if userId == self.maleId:
                to = self.femaleId
                prefix = "👦:"
            else:
                to = self.maleId
                prefix = "👩:"
            if token != userId: client.push_message(to, TextSendMessage(text=prefix+"定好約會囉，約會那天再聊吧"))
            if token != userId: client.reply_message(token, TextSendMessage(text=replytext))
        elif STAT ==30:
            replytext = "時間還沒到，不能跟對象聊天唷"
            if token != userId: client.reply_message(token, TextSendMessage(text=replytext))
        else :
            if token != userId: client.reply_message(token, TextSendMessage(text=replytext))
        self.save()
        return replytext


def getDate(userId):
    qMale = Date.objects(maleId = userId)
    qFemale = Date.objects(femaleId = userId)
    if qMale:
        return Date.objects.get(maleId = userId)
    elif qFemale:
        return Date.objects.get(femaleId = userId)
    else :
        return None
