import unittest,inspect

from linebot.models import events,messages,sources
import app
import cluster


class TestFunction(unittest.TestCase):
    """scope:男生約會流程"""
    """userId & replytoken = inspect.currentframe().f_code.co_name (aka current fuct name)
    第二個 userId =inspect.currentframe().f_code.co_name+'G'
    for status 123 因為還沒創建資料，所以要用 app 回傳 json 判斷正確性
    t_member ：測試用帳號 var 名稱
    t_date   ：測試用約會
    """
    @classmethod
    def setUpClass(cls):
        # clean
        for function in inspect.getmembers(cls, predicate=inspect.isfunction):
            if function[0].find('test_') != -1 :
                name = function[0]
                if cluster.getUser(name):cluster.getUser(name).delete()
                if cluster.getUser(name+"G"):cluster.getUser(name+"G").delete()
                if cluster.getDate(name):cluster.getDate(name).delete()
                if cluster.getDate(name+"G"):cluster.getDate(name+"G").delete()
        cls.client = app.app.test_client()
    @classmethod
    def tearDownClass(cls):
        # clean database
        return

    def test_約她(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=100).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name+"G", status=10).save()
        dict = {}
        self.postBackRequestDict(dict, inspect.currentframe().f_code.co_name+"G", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "成功邀約，對象會在24小時內回覆")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 110)
        t_memeber.delete()
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name+"G")
        self.assertIn(inspect.currentframe().f_code.co_name , t_date.invList)
        self.assertEqual(t_date.status, 11)
        t_date.delete()

    def test_討論好餐廳和時間了(self):
        t_member = cluster.Male(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name + "G",
                     maleId=inspect.currentframe().f_code.co_name , status=20).save()
        dict = {}
        self.messageRequestDict(dict, "討論好餐廳和時間了",inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<inLIne定位資訊>")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status,21)
        t_date.delete()
        t_member.delete()

    def test_敲定時間地點(self):
        t_member = cluster.Male(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name + "G",
                     maleId=inspect.currentframe().f_code.co_name, status=21).save()
        dict = {}
        self.messageRequestDict(dict, "<"+"https://inline.app/reservations/-MYykIBSxYNLzWg4ZgtI"+">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "關閉聊天，約會前12hr會開啟")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.inlineRes,"https://inline.app/reservations/-MYykIBSxYNLzWg4ZgtI")
        self.assertEqual(t_date.status, 30)
        t_date.delete()
        t_member.delete()

    def test_約會成功(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Female(userId=inspect.currentframe().f_code.co_name + "G", status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name + "G",
                     maleId=inspect.currentframe().f_code.co_name, status=40).save()
        dict = {}
        self.messageRequestDict(dict, "我出發了", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "祝您約會順利")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status, 50)
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 100)
        t_memeber.delete()
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name+"G")
        self.assertEqual(t_memeber.status, 100)
        t_memeber.delete()
        t_date.delete()

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

    def postBackRequestDict(self,dict,data,user_id_token):
        dict["destination"] = "testscript"
        dict["events"] = [events.PostbackEvent(postback=events.Postback(data),
                                              reply_token=user_id_token,
                                              source=sources.SourceUser(user_id=user_id_token)).__dict__]
        for event in dict["events"]:
            event['source'] = event['source'].__dict__
            event["postback"] =event["postback"].__dict__
            event['replyToken'] = event['reply_token']
            event['source']['userId'] = event['source']['user_id']


if __name__ == '__main__':
    unittest.main()