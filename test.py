import unittest,requests,subprocess,json

import flask,threading

import app


class TestFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.domain = "http://localhost:5000"
        cls.client = app.app.test_client()
        app.Course(NAME="課程1").save()
        app.Course(NAME="課程2").save()
        app.Course(NAME="課程3").save()
        app.Course(NAME="課程4").save()
    @classmethod
    def tearDownClass(cls):
        # clean database
        for obj in app.Course.objects():
            obj.delete()

    def test_courseC(self):
        newcourse = app.Course(NAME="性愛吹吹吹")
        response = self.client.put('/course',data=newcourse.to_mongo() )
        result = app.Course.objects(NAME = "性愛吹吹吹")
        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(result)
    def test_courseR(self):
        app.Course(NAME="讀龍課程").save()
        app.Course(NAME="讀龍鑽研課程").save()
        response  = self.client.get('/course')
        allcourse = app.Course.objects()
        self.assertEqual(response.status_code, 200)
        for course in allcourse:
            courseName = course.to_mongo()["NAME"]
            isIn = False
            for ele in response.json:
                if ele["NAME"] == courseName:isIn = True
            self.assertTrue(isIn)

    def test_courseD(self):
        delcourse = app.Course(NAME = "刪掉我")
        delcourse.save()
        response = self.client.delete('/course',data = delcourse.to_mongo())
        self.assertEqual(response.status_code, 200)
        result = app.Course.objects(NAME = "幹幹幹")
        self.assertFalse(result)
    def test_courseU(self):
        sbbb = app.Course.objects().first()
        sbbb["NAME"]="壞妹妹教學"
        response = self.client.post('/course',data = sbbb.to_mongo())
        self.assertEqual(response.status_code, 200)
        result = app.Course.objects(NAME = "壞妹妹教學")
        self.assertTrue(result)
if __name__ == '__main__':
    unittest.main()