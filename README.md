# loveletter-spider
loveletter spider, it crawls xiaohan love letter wall.

# usage
1. install [python 3.x](https://www.python.org)
2. install scrapy
```bash
pip install scrapy
```
3. run scrapy crawl command
```bash
scrapy crawl loveletter-xiaohan -o loveletter-`date +%Y.%m.%d-%H:%M:%S\`.json --logfile=loveletter-\`date +%Y.%m.%d-%H:%M:%S\`.log
```
note: you need to get the `wechat key` and `wechat_appmsg_token`
that can be extract from xiaohan wechat subscription link like follow:
```
https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MjEyODU2MA==&f=json&offset=0&count=10&is_ok=1&scene=124&uin=MTUyNzUyMTA3Mw%3D%3D&key=${wechat_key}&pass_ticket=K9t7oVL4QBgxPtPRwoUk5g2YTodNqOatojRvwwPSry%2FiDAqqGcW2R5WMIh2MuPzM&wxtoken=&appmsg_token=${wechat_appmsg_token}&f=json
```
and then the spider will be auto detect and fetch latest loveletter wall page.

ofcourse, you can just put the last loveletter wall page link on it. 
# aims
1. servitization
