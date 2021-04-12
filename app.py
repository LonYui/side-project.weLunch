from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask import request

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
    json_data = Course.objects().to_json()
    return json_data

@app.route("/course/<name>",methods=['GET'])
def getCourseByName(name):
    json_data = Course.objects(NAME = name).to_json()
    return json_data
@app.route("/course",methods=['PUT'])
def putCourse():
    newC = Course(NAME = request.form["NAME"])
    newC.save()
    return newC.to_json()
@app.route("/course",methods=['POST'])
def postCourse():
    courses  = Course.objects(id = request.form["id"])
    for course in courses:
        course.update(set__NAME=request.form["NAME"])

    return courses.to_json()
@app.route("/course",methods=['DELETE'])
def delCourse():
    courses = Course.objects(id = request.form["id"]).delete()
    return courses.to_json()

if __name__ == '__main__':
    app.run()
