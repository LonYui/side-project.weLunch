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
                if cluster.getDate(name):cluster.getDate(name).delete()
        cls.client = app.app.test_client()
    @classmethod
    def tearDownClass(cls):
        # clean database
        return

    def test_約她(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=100).save()
        cluster.Female(userId=inspect.currentframe().f_code.co_name+"G", status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name+"G", status=10).save()
        dict = {}
        self.postBackRequestDict(dict, {"userId":inspect.currentframe().f_code.co_name+"G"}, inspect.currentframe().f_code.co_name)
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
        dict["events"] = [events.PostbackEvent(postback=data,
                                              reply_token=user_id_token,
                                              source=sources.SourceUser(user_id=user_id_token)).__dict__]


if __name__ == '__main__':
    unittest.main()