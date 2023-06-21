## Weibo Trending Grab

http://101.35.156.253:8041/

### Video demo

[View it here](https://share.vidyard.com/watch/6oTwbNRcxgASFTnYmCRkZm?)

### Introduction
This is a personal project which involves front-end, back-end, and web crawler implementation. It grabs data periodically and store them in the database, then present to users with data visualization tool.

#### What data we fetch

Similar to Twitter, Weibo has its own trending list, describing what is being most searched on the platform. That 's what we are targeting for. We deploy a web crawler on the server, and it will automatically visit and fetch the [trending list of Weibo](https://www.weibo.com/newlogin?tabtype=search&gid=&openLoginLayer=0&url=) every 15 minutes.

#### After we fetch them

We store the fetched data (title, number of visits, index, timestamp...) in the database. We partitioned the tables to reduce the load.

#### How do we present them

When users visit our website, they can choose the date and time, then they will be presented with the trending list of that timestamp. After they click on each trend, they will be directed to a visualized graph, depicting how the index of this trend has gone throughout the day. 

#### Summary of tech stack

| Feature    | Framework |
| -------- | ------- |
| Web crawler  | Python + Selenium + Chromedriver    |
| Front-end | Js + Element UI + React.js    |
| Back-end    | Spring Boot + Mybatis    |
| Database    | MySQL    |
| Data Visualization    | Echarts    |



