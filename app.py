from flask import Flask, render_template, jsonify
from flask_mongoengine import MongoEngine
from flask import request
import json

from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "host":"mongodb+srv://Tsung:d39105648@cluster0.dmjou.mongodb.net/Cluster0?retryWrites=true&w=majority"
}
db = MongoEngine(app)

import mongoengine as me

class Course(me.Document):
    NAME = me.StringField(required=True)
    meta = {'collection': 'COURSE',"strict":False }

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template('hi.html', name=username)


@app.route("/course",methods=['GET'])
def getCourse():
    data = Course.objects()
    return jsonify([json.loads(ele.to_json()) for ele in data])

@app.route("/course/<name>",methods=['GET'])
def getCourseByName(name):
    data = Course.objects(NAME = name)
    return jsonify([json.loads(ele.to_json()) for ele in data])
@app.route("/course",methods=['PUT'])
def putCourse():
    newC = Course(NAME = request.form["NAME"])
    newC.save()
    return json.loads(newC.to_json())
@app.route("/course",methods=['POST'])
def postCourse():
    course = Course.objects().get(id = request.form["_id"])
    # TODO how to handle muiltiple column?
    data = request.form
    for key, value in data.items():
        if(key[0]!="_"):course[key]=value
    course.save()
    return json.loads(course.to_json())
@app.route("/course",methods=['DELETE'])
def delCourse():
    Course.objects().get(id = request.form["_id"]).delete()
    return "del success"
@app.route("/webhook",methods=['POST'])
def webhook():
    client = LineBotApi("jpkaZF4J41V3hTOT7kinpR16tTormHg0pKDpr5UJX6sOyeIETiHnXOYveDupNa6Zk6KKE1B+zZSiKQJ8qSrGVCeDD2EEsRzXeOEImKtQfrU1UjvLysgAvcRoGpMVos79emD+gZT3uJvF1O2pLJIQkgdB04t89/1O/w1cDnyilFU=")
    rJson = request.json
    for event in rJson["events"]:
        client.reply_message(event["replyToken"],TextSendMessage(text=event["message"]["text"]))
    return "ok"


if __name__ == '__main__':
    app.run()
