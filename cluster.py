import mongoengine as me
from mongoengine import connect
from datetime import  date as DT,timedelta
from linebot.models import actions,template

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
    inlineRes = me.URLField()

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
               ("dateDate", "成功發起約會")

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
        attr = tup[STAT][0]
        # 處理 status 變換
        setattr(self, attr, reqstext)
        self.status += 1
        if STAT == 5:
            self.status = 10
        replytext = tup[STAT][1]
        # 處理 replyMessage
        if STAT in (1, 2, 3, 4):
            action1 = actions.MessageAction(text=tup[STAT][2][0], label=tup[STAT][2][0])
            action2 = actions.MessageAction(text=tup[STAT][2][1], label=tup[STAT][2][1])
            action3 = actions.MessageAction(text=tup[STAT][2][2], label=tup[STAT][2][2])
            column = template.CarouselColumn(text=replytext, actions=[action1, action2, action3])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                          alt_text="broke")])
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
