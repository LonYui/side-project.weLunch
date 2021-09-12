# 摘要 Description

參考 Let's movie，午餐約會 bot 做為後端展示作品,  練習 Tdd 順便學 flask。

A dating service chatbot on Line platform.

# Demo


https://user-images.githubusercontent.com/9551862/132978460-73640b9c-a34f-44b5-bfcc-b79361251fbc.mov



# 索引

* [使用技術/practice tech](#a)
* [bot 介紹](#b)
  * [特色/Feature](#b1)
  * [功能/Function](#b2)
  * [使用說明書](#b3)
* [coverage report](#c1)

<h1 id="a">使用技術/practice tech</h1>

- TDD - Write acceptance test before start dev.
- Git
  - Write commit message with type, title and body. Answering what, why, how .
  - Use github issue track probleam.
- 3-rd api & Package - Flask, Line Message, Mongoengine, Heroku
- Doc - Using more index, graph. Describe the probleam rather than answer it.


<h1 id="b">bot 介紹</h1>

信義區、內科上班族，用午休時間來交朋友

<h2 id="b1">特色</h2>

1. 直接約見面
2. 使用零碎時間
3. 以吃會友
4. 一次只能約一個
5. 商業午餐實惠

Feature
- Easy hangout
- Use workday lunchtime to social
- Normal day restaurant has discount

<h2 id="b2">功能</h2>

1. 即時聊天
2. 觀看交友名片
3. 配對

Function
- chatroom
- Tinder-like info card
- match

<h2 id="b3">使用說明書</h2>

<img src="https://i.imgur.com/OBkbD0J.png" width="100" height="100">

1. 掃秒加入好友 weDateApp
2. 註冊好友輸入基本資料、照片 url 
3. 注意！驗證碼為 iampassword（因為：api 簡訊還沒串）
4. 然後等待審核，（開通請通知我一聲）

然後就可以開始約會啦

第一次 call 要等 10 秒（因為：server 使用 heroku 免費專案）

# 其他詳情請看規格書.pdf
<h2 id="c1">coverage report 9/9</h2>

```
Name                                                                               Stmts   Miss  Cover  
----------------------------------------------------------------------------------------------------------------
app.py                                                                               120     41    66%  
cluster.py                                                                           269     49    82%
```
