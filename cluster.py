import mongoengine as me
from mongoengine import connect

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
