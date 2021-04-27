# 摘要

參考 wemovie bot，午餐約會 bot 做為後端展示作品,  練習 Tdd 順便學 flask。

# 使用技術

- TDD - 用 unittest 寫驗收測試再開發程式
- git 
  \- write commit message with type,title and body by [this](https://wadehuanglearning.blogspot.com/2019/05/commit-commit-commit-why-what-commit.html) rule 
  \- use issue track probleam
- flask - use mongoengine do orm ,物件導向程式設計
- 3方 api 串接
  \- line
  \- heroku
- 使用策略模式處理累贅is elif判斷 commit [ticket](https://github.com/d5269357812/weLunch/commit/fb2677aeab5f84953f345599be7a5d0839199aa0)
- 壓力測試 - 常用 api 使用 locust測試（TODO）
- 規格撰寫 - 索引頁、多用圖片、形容問題而非解答。參照[此](https://stackoverflow.com/questions/379371/what-makes-a-good-spec)

# bot 介紹

信義區、內科上班族，用午休時間來交朋友

### 特色

1. 直接約見面
2. 使用零碎時間
3. 以吃會友
4. 一次只能約一個
5. 商業午餐實惠

### 功能

1. 即時聊天
2. 觀看交友名片
3. 配對

### 使用說明書



1. 掃秒加入好友 weDateApp
2. 註冊好友輸入基本資料、照片url 
3. 注意！驗證碼為 iampassword（因為：api 簡訊還沒串）
4. 然後等待審核，（開通請通知我一聲）

然後就可以開始約會啦

第一次 call 要等 10 秒（因為：server 使用 heroku 免費專案）

# 其他詳情請看規格書.pdf

