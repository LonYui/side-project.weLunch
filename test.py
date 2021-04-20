import unittest,inspect

from linebot.models import events,messages,sources
from datetime import date
import app
import cluster


class TestFunction(unittest.TestCase):
    """userId & replytoken = inspect.currentframe().f_code.co_name (aka current fuct name)
    TODO：input event 只能是 message
    for status 123 因為還沒創建資料，所以要用 app 回傳 json 判斷正確性
    t_member ：測試用帳號 var 名稱
    """
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
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 3)
        t_memeber.delete()
    def test_選擇性別女(self):
        dict = {}
        self.messageRequestDict(dict, "女生", inspect.currentframe().f_code.co_name)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "注意：需用<>標記訊息")
        t_memeber =  cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status,3)
        t_memeber.delete()
    def test_教學框(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name,status=3).save()
        dict = {}
        self.messageRequestDict(dict,"好",inspect.currentframe().f_code.co_name)
        response = self.client.post('/',json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<名字>")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status,4)
        t_memeber.delete()
    def test_名字(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name,status=4).save()
        nickName = "阿蟲"
        dict = {}
        self.messageRequestDict(dict,"<"+nickName+">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<生日> (yyyy-mm-dd)")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 5)
        self.assertEqual(t_memeber.nickName,nickName)
        t_memeber.delete()
    def test_名字偵測不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name,status=4).save()
        nickName = "沒有標記名字"
        dict = {}
        self.messageRequestDict(dict,nickName, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 4)
        self.assertIsNone(t_memeber.nickName)
        t_memeber.delete()

    def test_生日(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=5).save()
        birthdate = "1995-03-25"
        dict = {}
        self.messageRequestDict(dict, "<" + birthdate + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "您是1995-03-25的牡羊座男孩嗎？")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 6)
        self.assertEqual(t_memeber.birthDate.isoformat(), birthdate)
        t_memeber.delete()
    def test_生日偵測不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=5).save()
        birthdate = "沒有標記的日子"
        dict = {}
        self.messageRequestDict(dict, birthdate, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 5)
        self.assertIsNone(t_memeber.birthDate)
        t_memeber.delete()

    def test_生日confirm(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=6).save()
        dict = {}
        self.messageRequestDict(dict,"沒錯", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<個人特質>")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 7)
        t_memeber.delete()
    def test_生日confirm不是(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=6,birthDate=date.fromisoformat("1111-11-11")).save()
        dict = {}
        self.messageRequestDict(dict, "不是", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 5)
        self.assertIsNone(t_memeber.birthDate)
        t_memeber.delete()
    def test_一項個人特質(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=7).save()
        personality = "懶惰"
        dict = {}
        self.messageRequestDict(dict, "<" + personality + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<興趣>")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 8)
        self.assertEqual(t_memeber.personality, personality)
        t_memeber.delete()
    def test_一項個人特質偵測不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=7).save()
        personality = "沒標記的個性"
        dict = {}
        self.messageRequestDict(dict, personality, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 7)
        self.assertIsNone(t_memeber.personality)
        t_memeber.delete()

    def test_興趣10word(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=8).save()
        hobit = "釣魚"
        dict = {}
        self.messageRequestDict(dict, "<" + hobit + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<職業>")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 9)
        self.assertEqual(t_memeber.hobit, hobit)
        t_memeber.delete()
    def test_興趣找不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=8).save()
        hobit = "沒有標記的興趣"
        dict = {}
        self.messageRequestDict(dict, hobit, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 8)
        self.assertIsNone(t_memeber.hobit)
        t_memeber.delete()

    def test_職業(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=9).save()
        job = "工程師"
        dict = {}
        self.messageRequestDict(dict, "<" + job + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<照片url>")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 10)
        self.assertEqual(t_memeber.job, job)
        t_memeber.delete()
    def test_職業找不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=9).save()
        job = "沒有標記的職業"
        dict = {}
        self.messageRequestDict(dict, job, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 9)
        self.assertIsNone(t_memeber.job)
        t_memeber.delete()

    def test_照片(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=10).save()
        pictUri = "https://i.imgur.com/aVyjw87"
        dict = {}
        self.messageRequestDict(dict, "<" + pictUri + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<信箱>")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 11)
        self.assertEqual(t_memeber.pictUri, pictUri)
        t_memeber.delete()
    def test_照片找不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=10).save()
        pictUri = "網址沒有標記"
        dict = {}
        self.messageRequestDict(dict, pictUri, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 10)
        self.assertIsNone(t_memeber.pictUri)
        t_memeber.delete()

    # def test_照片_格式錯誤(self):
    #     cluster.Male(userId=inspect.currentframe().f_code.co_name, status=10).save()
    #     pictUri = "我不是網址"
    #     dict = {}
    #     self.messageRequestDict(dict, "<" + pictUri + ">", inspect.currentframe().f_code.co_name)
    #     response = self.client.post('/', json=dict)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data.decode("utf-8"), "不是正確url")
    #     t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
    #     self.assertEqual(t_memeber.status, 10)
    #     self.assertIsNone(t_memeber.pictUri)
    #     t_memeber.delete()

    # def test_照片_url404(self):
    #     cluster.Male(userId=inspect.currentframe().f_code.co_name, status=10).save()
    #     pictUri = "https://cdn2.ettoday.net/images/404/cannotFind.jpg"
    #     dict = {}
    #     self.messageRequestDict(dict, "<" + pictUri + ">", inspect.currentframe().f_code.co_name)
    #     response = self.client.post('/', json=dict)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data.decode("utf-8"), "照片網址無法開啟")
    #     t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
    #     self.assertEqual(t_memeber.status, 10)
    #     self.assertIsNone(t_memeber.pictUri)
    #     t_memeber.delete()

    def test_信箱(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=11).save()
        email = "d5269357812@gmail.com"
        dict = {}
        self.messageRequestDict(dict, "<" + email + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<電話>")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 12)
        self.assertEqual(t_memeber.email, email)
        t_memeber.delete()
    def test_信箱找不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=11).save()
        email = "我沒有標記@gmail.com"
        dict = {}
        self.messageRequestDict(dict, email, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 11)
        self.assertIsNone(t_memeber.email)
        t_memeber.delete()

    # def test_信箱_格式錯誤(self):
    #     cluster.Male(userId=inspect.currentframe().f_code.co_name, status=11).save()
    #     email = "我不是信箱"
    #     dict = {}
    #     self.messageRequestDict(dict, "<" + email + ">", inspect.currentframe().f_code.co_name)
    #     response = self.client.post('/', json=dict)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data.decode("utf-8"), "email格式錯誤")
    #     t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
    #     self.assertEqual(t_memeber.status, 11)
    #     self.assertIsNone(t_memeber.email)
    #     t_memeber.delete()
    def test_電話(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=12).save()
        phone = "0919547381"
        dict = {}
        self.messageRequestDict(dict, "<" + phone + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "請輸入<驗證碼>，查看手機簡訊")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 13)
        self.assertEqual(t_memeber.phone, phone)
        t_memeber.delete()
    def test_電話找不到標記(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=12).save()
        phone = "電話沒有標記"
        dict = {}
        self.messageRequestDict(dict, phone, inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "偵測不到<>，請再試一次")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 12)
        self.assertIsNone(t_memeber.phone)
        t_memeber.delete()

    # def test_電話格式錯誤(self):
    #     cluster.Male(userId=inspect.currentframe().f_code.co_name, status=12).save()
    #     phone = "我不是電話號碼"
    #     dict = {}
    #     self.messageRequestDict(dict, "<" + phone + ">", inspect.currentframe().f_code.co_name)
    #     response = self.client.post('/', json=dict)
    #     self.assertEqual(response.status_code, 200)
    #     t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
    #     self.assertEqual(t_memeber.status, 12)
    #     self.assertIsNone(t_memeber.phone)
    #     self.assertEqual(response.data.decode("utf-8"), "電話號碼格式錯誤")
    #     t_memeber.delete()
    def test_輸入驗證碼(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=13,nickName="阿諺",personality="開朗",hobit="做愛",pictUri="https://i.imgur.com/9FEddMc.jpg").save()
        validateCode = "iampassword"
        dict = {}
        self.messageRequestDict(dict, "<" + validateCode + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "最後確認，這樣資料正確嗎？")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 14)
        t_memeber.delete()
    def test_輸入錯誤的驗證碼(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=13).save()
        validateCode = "錯誤密碼"
        dict = {}
        self.messageRequestDict(dict, "<" + validateCode + ">", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "錯誤，請再輸入一次手機")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 12)
        self.assertIsNone(t_memeber.phone)
        t_memeber.delete()
    def test_照片confirm(self):
        cluster.Male(userId=inspect.currentframe().f_code.co_name, status=14).save()
        dict = {}
        self.messageRequestDict(dict, "確認", inspect.currentframe().f_code.co_name)
        response = self.client.post('/', json=dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "待審核後就可以開始使用了")
        t_memeber = cluster.getUser(inspect.currentframe().f_code.co_name)
        self.assertEqual(t_memeber.status, 15)
        t_memeber.delete()
    # TODO confirm不是的流程借用帳號再次跑一遍

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