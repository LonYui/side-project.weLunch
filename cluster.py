from datetime import date as dt
import mongoengine as me,re
from mongoengine import connect
from datetime import  date as DT,timedelta
from linebot.models import actions,template,TextSendMessage

connect(host ="mongodb+srv://Tsung:d39105648@restaurant.m9bx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" )
class Member(me.Document):
    meta = {
        'abstract': True,
    }
    def isMale(self):
        if self.__class__.__name__ == "Male":
            return True
        elif self.__class__.__name__ == "Female":
            return False
    def signup(self,reqsT,client,token):
        """
        只處理 status += 1 的流程
        status not change 和 status -=1 情況當作例外處理 （regex , 6, 13等 共3處）
        """
        tup =(
            (),(),(),
            # status3
            (None,"請輸入<名字>"),
            ("nickName","請輸入<生日> (yyyy-mm-dd)"),
            ("birthDate",None,("沒錯","剛剛手滑了")),
            (None,"請輸入<個人特質>"),
            ("personality","請輸入<興趣>"),
            ("hobit","請輸入<職業>"),
            ("job","請輸入<照片url>"),
            # status10
            ("pictUri","請輸入<信箱>"),
            ("email","請輸入<電話>"),
            ("phone","請輸入<驗證碼>，查看手機簡訊"),
            (None,"最後確認，這樣資料正確嗎？",("沒錯",)),
            (None,"待審核後就可以開始使用了"),
        )
        STAT = self.status

        if tup[STAT][0]:
            m = re.search("<(\\S+)>", reqsT)
            if not m:
                """status not change"""
                if token != self.userId:
                    client.reply_message(
                        token, TextSendMessage(text="偵測不到<>，請再試一次"))
                return "偵測不到<>，請再試一次"
            else:
                reqsT = m.groups()[0]
        if STAT in (6,) and reqsT in ["不是", "剛剛手滑了", "n"]:
            """status -1 """
            self.status -= 1
            self.birthDate = None
            self.save()
            if token != self.userId:
                client.reply_message(token, TextSendMessage(text="請輸入<生日> (yyyy-mm-dd)"))
            return "請輸入<生日> (yyyy-mm-dd)"
        if STAT in (13,) and reqsT not in ["iampassword",]:
            """status -1 """
            self.status -= 1
            self.phone = None
            self.save()
            if token != self.userId:
                client.reply_message(token, TextSendMessage(text="錯誤，請再輸入一次手機"))
            return "錯誤，請再輸入一次手機"

        # 處理assign Value

        if STAT == 5:
            reqsT = dt.fromisoformat(reqsT)

        attr = tup[STAT][0]
        if attr :setattr(self, attr, reqsT)
        # 處理 status 變換
        self.status += 1
        # 處理 replyMessage sendmesg
        replyT,sendMsg = tup[STAT][1],TextSendMessage(text=tup[STAT][1])
        if STAT == 5:
            replyT = "您是" + self.birthDate.isoformat() \
                     + "的" + getConstellation(
                self.birthDate.month, self.birthDate.day)
            if self.isMale():
                replyT += "男孩嗎？"
            else:
                replyT += "女孩嗎？"

            action1 = actions.MessageAction(text=tup[STAT][2][0], label=tup[STAT][2][0])
            action2 = actions.MessageAction(text=tup[STAT][2][1], label=tup[STAT][2][1])
            column = template.CarouselColumn(
                text=replyT, actions=[action1, action2])
            carouse = template.CarouselTemplate(columns=[column])
            sendMsg = [template.TemplateSendMessage(template=carouse,alt_text="broke")]
        elif STAT == 13:
            introT = "個性" + self.personality \
                   + "喜歡" + self.hobit + "的" + \
                   getConstellation(
                       self.birthDate.month, self.birthDate.day) + "男孩"
            if self.isMale():
                introT += "男孩"
            else:
                introT += "女孩"
            action = actions.MessageAction(text=tup[STAT][2][0], label=tup[STAT][2][0])
            column = template.CarouselColumn(
                title=self.nickName, text=introT,
                thumbnail_image_url=self.pictUri, actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            sendMsg = [TextSendMessage(text=replyT),template.TemplateSendMessage(template=carouse,alt_text="break")]
        self.save()
        if token != self.userId:
            client.reply_message(token, sendMsg)
        return replyT

class Male(Member):
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

    def readDate(self,token,userId,client):
        """觀看約會"""
        colLis = []
        for dating in Date.objects(status = 10):
            girl = getUser(dating.femaleId)
            action = actions.PostbackAction(
                data=dating.femaleId, label="邀請她",
                display_text="邀請她")
            column = template.CarouselColumn(
                actions=[action],
                title=str(calculate_age(girl.birthDate))
                      + "," + girl.nickName,
                text="我在" + dating.workDist + "上班，喜歡"
                     + dating.eatype + "，拜"
                     + str(dating.dateDate.isoweekday()) + "有空嗎？",
                thumbnail_image_url=girl.pictUri, )
            colLis.append(column)
        if colLis == []:
            if token != userId:
                client.reply_message(token, TextSendMessage(text='目前無約會'))
            return
        carouse = template.CarouselTemplate(columns=colLis)
        if token != userId:
            client.reply_message(
                token, [template.TemplateSendMessage(
                    template=carouse, alt_text="broke")])
        return

class Female(Member):
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

    def createDate(self):
        """發起約會"""
        replyT = "上班在哪一區呀？"
        Date(femaleId=self.userId, status=1).save()
        self.status += 10
        self.save()
        return replyT

    def readInvList(self,token,userId,client):
        """觀看邀請名單"""
        colLis = []
        date = getDate(self.userId)
        for invId in date.invList:
            user = getUser(invId)
            text = "個性" + user.personality \
                   + "喜歡" + user.hobit + "的" + \
                   getConstellation(
                       user.birthDate.month, user.birthDate.day) \
                   + "男孩"
            action = actions.PostbackAction(data=invId, label="選他",
                                            display_text="選他")
            column = template.CarouselColumn(
                title=user.nickName, text=text,
                thumbnail_image_url=user.pictUri, actions=[action])
            colLis.append(column)
        carouse = template.CarouselTemplate(columns=colLis)
        if token != userId:
            client.reply_message(
                token, [template.TemplateSendMessage(
                    template=carouse, alt_text="broke")])
        return


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

    def assignValue(self, reqsT, userId, token, client):
        tup = ("","workDist","lunchBreakT","lunchBreakL","eatype","dateDate","","","","",
               "invList","maleId","","","","","","","","",
               None,"inlineRes","","","","","","","","",
               None,"","","","","","","","","",
               None,
               )
        STAT = self.status
        if  STAT== 3:
            reqsT = reqsT[3:]
        elif STAT == 5:
            if reqsT == "明天":
                reqsT = DT.today() + timedelta(days=1)
            elif reqsT == "後天":
                reqsT = DT.today() + timedelta(days=2)
            elif reqsT == "大後天":
                reqsT = DT.today() + timedelta(days=3)
        elif STAT in (10,11) and getUser(reqsT) is None:
            reqsT = None
        elif STAT ==30:
            reqsT = None
        elif STAT ==21:
            m = re.search("<(\S+)>", reqsT)
            if not m:
                if token != userId: client.reply_message(token, TextSendMessage(text="偵測不到<>，請再試一次"))
                return "偵測不到<>，請再試一次"
            reqsT = m.groups()[0]
        else:pass
        attr = tup[STAT]
        if attr is None or reqsT is None:pass
        elif attr == 'invList':
            self[attr].append(reqsT)
        elif attr == 'maleId':
            self.invList.remove(reqsT)
            setattr(self, attr, reqsT)
        else:
            setattr(self, attr, reqsT)
        self.save()
        return

    def statusChange(self, reqsT):
        STAT = self.status
        if STAT in (1,2,3,4):self.status += 1
        elif STAT == 5:self.status = 10
        elif STAT == 10 and getUser(reqsT) is not None:self.status += 1
        elif STAT == 11 and  getUser(reqsT) is not None:self.status = 20
        elif STAT == 20 and reqsT == "討論好餐廳和時間了":self.status += 1
        elif STAT == 21:self.status = 30
        elif STAT == 40 and reqsT == "我出發了":
            self.status = 50
            boy = getUser(self.maleId)
            girl = getUser(self.femaleId)
            boy.status = 100
            girl.status = 100
            boy.save()
            girl.save()
        else:pass
        self.save()
        return

    def replyText(self, token, userId, reqsT, client):
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

        STAT = self.status
        replytext = tup[STAT][1]
        if STAT in (1, 2, 3, 4):
            action1 = actions.MessageAction(text=tup[STAT][2][0],
                                            label=tup[STAT][2][0])
            action2 = actions.MessageAction(text=tup[STAT][2][1],
                                            label=tup[STAT][2][1])
            action3 = actions.MessageAction(text=tup[STAT][2][2],
                                            label=tup[STAT][2][2])
            column = template.CarouselColumn(text=replytext,
                                             actions=[action1, action2,
                                                      action3])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, [
                template.TemplateSendMessage(template=carouse,
                                             alt_text="broke")])
        elif STAT in (10,) and getUser(reqsT) is None:
            replytext = "無人邀請"
        elif STAT in (11,) and getUser(reqsT) is None:
            replytext = "有人邀約了"
            action = actions.MessageAction(text="觀看邀請名單",
                                           label="觀看邀請名單")
            column = template.CarouselColumn(text=replytext,
                                             actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token, [
                template.TemplateSendMessage(template=carouse,
                                             alt_text="broke")])
            return replytext
        elif STAT in (11,):
            action = actions.MessageAction(text=tup[STAT][2][0],
                                           label=tup[STAT][2][0])
            column = template.CarouselColumn(text=replytext,
                                             actions=[action])
            carouse = template.CarouselTemplate(columns=[column])
            if token != userId: client.reply_message(token,
                                                     TextSendMessage(
                                                         text=replytext))
            if token != userId: client.push_message(self.maleId, [
                template.TemplateSendMessage(template=carouse,
                                             alt_text="broke")])
        elif STAT in (20, 40) and reqsT not in ("討論好餐廳和時間了", "我出發了"):
            to, prefix = ("", "")
            if userId == self.maleId:
                to = self.femaleId
                prefix = "👦:"
            else:
                to = self.maleId
                prefix = "👩:"
            if token != userId: client.push_message(to, TextSendMessage(
                text=prefix + reqsT))
            return reqsT
        elif STAT == 20:
            to, prefix = ("", "")
            if userId == self.maleId:
                to = self.femaleId
                prefix = "👦:"
            else:
                to = self.maleId
                prefix = "👩:"
            if token != userId: client.push_message(to, TextSendMessage(
                text=prefix + "定好約會囉，約會那天再聊吧"))
            if token != userId: client.reply_message(token,
                                                     TextSendMessage(
                                                         text=replytext))
        elif STAT == 30:
            replytext = "時間還沒到，不能跟對象聊天唷"
            if token != userId: client.reply_message(token,
                                                     TextSendMessage(
                                                         text=replytext))
        else:
            if token != userId: client.reply_message(token,
                                                     TextSendMessage(
                                                         text=replytext))
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
