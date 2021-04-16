import unittest

from linebot.models import events,messages,sources

import app
import cluster


class TestFunction(unittest.TestCase):
    """user_id = __name__
    ＴＯＤＯ：input event 只能是 message"""
    @classmethod
    def setUpClass(cls):
        cls.client = app.app.test_client()
    @classmethod
    def tearDownClass(cls):
        # clean database
        return

    def test_點選開始使用開始啟用您的個人資料(self):
        # status 0==1
        dict = {}
        self.messageRequestDict(dict, "開始使用", __name__)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"),"請輸入性別")
    def test_選擇性別男(self):
        dict = {}
        self.messageRequestDict(dict, "男生", __name__)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "注意：需用<>標記訊息")
        result = cluster.Male.objects(user_id=__name__)
        self.assertTrue(result)
        for male in result:
            male.delete()
    def test_選擇性別女(self):
        dict = {}
        self.messageRequestDict(dict, "女生", __name__)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "注意：需用<>標記訊息")
        result = cluster.Female.objects(user_id=__name__)
        self.assertTrue(result)
        for female in result:
            female.delete()
    def test_教學框(self):
        dict = {}
        self.messageRequestDict(dict,"好", __name__)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入名字")


    def messageRequestDict(self,dict,text,user_id_token):
        dict["destination"] = "testscript"
        dict["events"]=[events.MessageEvent(message=messages.TextMessage(text=text),
                                            source=sources.SourceUser(user_id=user_id_token)).__dict__]
        for event in dict["events"]:
            event['source'] = event['source'].__dict__
            event['message'] = event['message'].__dict__
        return

if __name__ == '__main__':
    unittest.main()