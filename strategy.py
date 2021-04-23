import datetime
from linebot.models import actions,template

def ST_Dstatus(n,date,reqstext,userId,token,client):
    tup = ((),
           ("workDist", "幾點開始午休呢",("十二點","十二點半","一點")),
           ("lunchBreakT","午休時間很長嗎？",("普通，一小","還行，一小半","很長，兩小")),
           ("lunchBreakL","喜歡吃韓式還是日式",("日式","韓式","港式")),
           ("eatype","那約個明天、後天",("明天","後天","大後天")),
           ("dateDate","成功發起約會")

    )
    if n == 3:reqstext=reqstext[3:]
    if n == 5:
        if reqstext == "明天":
            reqstext = datetime.date.today() + datetime.timedelta(days=1)
        elif reqstext == "後天":
            reqstext = datetime.date.today() + datetime.timedelta(days=2)
        elif reqstext == "大後天":
            reqstext = datetime.date.today() + datetime.timedelta(days=3)
    attr = tup[n][0]
    setattr(date, attr, reqstext)
    date.status += 1
    if n==5:
        date.status = 10
    replytext = tup[n][1]

    if n in (1,2,3,4):
        action1 = actions.MessageAction(text=tup[n][2][0], label=tup[n][2][0])
        action2 = actions.MessageAction(text=tup[n][2][1], label=tup[n][2][1])
        action3 = actions.MessageAction(text=tup[n][2][2], label=tup[n][2][2])
        column = template.CarouselColumn(text=replytext, actions=[action1, action2,action3])
        carouse = template.CarouselTemplate(columns=[column])
        if token != userId: client.reply_message(token, [template.TemplateSendMessage(template=carouse,
                                                                                      alt_text="broke")])
    date.save()
    return replytext