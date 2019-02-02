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
# global
1. servitization