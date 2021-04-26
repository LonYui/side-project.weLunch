import unittest,inspect

from linebot.models import events,messages,sources
import app
import cluster,datetime


class TestFunction(unittest.TestCase):
    """scope:女生約會流程"""
    """userId & replytoken = inspect.currentframe().f_code.co_name (aka current fuct name)
    userId2 = inspect.currentframe().f_code.co_name +"M"
    TODO：input event 只能是 message
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

    def test_發起約會(self):
        cluster.Female(userId=inspect.currentframe().f_code.co_name, status=100).save()
        dict = {}
        self.messageRequestDict(dict, "發起約會", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "上班在哪一區呀？")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 110)
        t_memeber.delete()
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.femaleId, inspect.currentframe().f_code.co_name)
        t_date.delete()
    def test_選擇希望吃飯地區(self):
        t_member = t_member = cluster.Female(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name,status=1).save()
        dict = {}
        self.messageRequestDict(dict, "內湖科學園區", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "幾點開始午休呢")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status, 2)
        self.assertEqual(t_date.workDist,"內湖科學園區")
        t_date.delete()
        t_member.delete()
    def test_輸入午休時間(self):
        t_member = t_member = cluster.Female(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name,status = 2).save()
        dict = {}
        self.messageRequestDict(dict, "十二點半", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "午休時間很長嗎？")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status, 3)
        self.assertEqual(t_date.lunchBreakT, "十二點半")
        # t_memeber.delete()
    # def test_輸入午休長度(self):
    #     cluster.Female(userId=inspect.currentframe().f_code.co_name, status=14).save()
        dict = {}
        self.messageRequestDict(dict, "普通，一小半", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "喜歡吃韓式還是日式")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status, 4)
        self.assertEqual(t_date.lunchBreakL, "一小半")
        t_date.delete()
        t_member.delete()
    def test_許願池(self):
        t_member = cluster.Female(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name,status = 4).save()
        dict = {}
        self.messageRequestDict(dict, "港式", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "那約個明天、後天")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status, 5)
        self.assertEqual(t_date.eatype, "港式")
        t_date.delete()
        t_member.delete()
    def test_選擇日期(self):
        t_member = cluster.Female(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name,status = 5).save()
        dict = {}
        self.messageRequestDict(dict, "明天", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "成功發起約會")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status, 10)
        self.assertEqual(t_date.dateDate, datetime.date.today() + datetime.timedelta(days=1) )
        t_date.delete()
        t_member.delete()

    def test_沒有人約(self):
        t_member = cluster.Female(userId=inspect.currentframe().f_code.co_name, status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name, status=10).save()
        dict = {}
        self.messageRequestDict(dict, "隨便輸入訊息", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "無人邀請")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status,10)
        t_date.delete()
        t_member.delete()

    def test_有人約(self):
        t_member1 = cluster.Female(userId=inspect.currentframe().f_code.co_name, status=110).save()
        t_member2 = cluster.Male(userId=inspect.currentframe().f_code.co_name+"M", status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name, status=11,invList=[inspect.currentframe().f_code.co_name+"M"]).save()
        dict = {}
        self.messageRequestDict(dict, "隨便輸入訊息", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "有人邀約了")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status,11)
        t_date.delete()
        t_member1.delete()
        t_member2.delete()

    def test_選擇約會對象(self):
        t_member1 = cluster.Female(userId=inspect.currentframe().f_code.co_name,status=110).save()
        t_member2 = cluster.Male(userId=inspect.currentframe().f_code.co_name+"M",status=110).save()
        cluster.Date(femaleId=inspect.currentframe().f_code.co_name,
                     invList=[inspect.currentframe().f_code.co_name+"M"],status=11).save()
        dict = {}
        self.postBackRequestDict(dict, inspect.currentframe().f_code.co_name+"M", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "開放 12hr 聊天")
        t_date = cluster.getDate(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_date.status, 20)
        self.assertEqual(t_date.maleId,inspect.currentframe().f_code.co_name+"M")
        self.assertNotIn(inspect.currentframe().f_code.co_name+"M" , t_date.invList)
        t_date.delete()
        t_member1.delete()
        t_member2.delete()

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