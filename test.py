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

if __name__ == '__main__':
    unittest.main()