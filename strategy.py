import datetime


def ST_Dstatus(n,date,reqstext):
    tup = ((),
           ("workDist", "幾點開始午休呢"),
           ("lunchBreakT","午休時間很長嗎？"),
           ("lunchBreakL","喜歡吃韓式還是日式？"),
           ("eatype","那約明天、後天還是大後天？"),
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
    date.save()
    return replytext