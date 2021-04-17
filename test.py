import unittest,inspect

from linebot.models import events,messages,sources

import app
import cluster


class TestFunction(unittest.TestCase):
    """userId & replytoken = inspect.currentframe().f_code.co_name (aka current fuct name)
    ＴＯＤＯ：input event 只能是 message"""
    @classmethod
    def setUpClass(cls):
        # clean
        for function in inspect.getmembers(cls, predicate=inspect.isfunction):
            if function[0].find('test_') != -1 :
                name = function[0]
                if cluster.getUser(name):cluster.getUser(name).delete()
        cls.client = app.app.test_client()
    @classmethod
    def tearDownClass(cls):
        # clean database
        return

    def test_點選開始使用開始啟用您的個人資料(self):
        # status 0==1
        dict = {}
        self.messageRequestDict(dict, "開始使用", inspect.currentframe().f_code.co_name)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"),"請輸入性別")
    def test_選擇性別男(self):
        dict = {}
        self.messageRequestDict(dict, "男生", inspect.currentframe().f_code.co_name)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "注意：需用<>標記訊息")
        result = cluster.Male.objects(userId=inspect.currentframe().f_code.co_name)
        self.assertTrue(result)
        for male in result:
            male.delete()
    def test_選擇性別女(self):
        dict = {}
        self.messageRequestDict(dict, "女生", inspect.currentframe().f_code.co_name)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "注意：需用<>標記訊息")
        result = cluster.Female.objects(userId=inspect.currentframe().f_code.co_name)
        self.assertTrue(result)
        for female in result:
            female.delete()
    def test_教學框(self):
        dict = {}
        self.messageRequestDict(dict,"好",inspect.currentframe().f_code.co_name)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入名字")


    def messageRequestDict(self,dict,text,user_id_token):
        """package是下劃線,json格式應為駝峰"""
        dict["destination"] = "testscript"
        dict["events"]=[events.MessageEvent(message=messages.TextMessage(text=text),
                                            reply_token=user_id_token,
                                            source=sources.SourceUser(user_id=user_id_token)).__dict__]
        for event in dict["events"]:
            event['source'] = event['source'].__dict__
            event['message'] = event['message'].__dict__
            event['replyToken']=event['reply_token']
            event['source']['userId']=event['source']['user_id']
        return

if __name__ == '__main__':
    unittest.main()