# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from loveletter.parsers import CardStyleParser, BoxStyleParser, TextStyleParser
from loveletter.loaders import LoveLetterLoader, LoveThemeLoader

class LoveLetterSpider(scrapy.Spider):
    name = 'loveletter-xiaohan'
    wechat_key = '6d1e78dd2153a25082d38f2fbfbd097e0a7532fa8a60400ab11ead91eef6bc05c12ccb09a49befbf254a3c2e6b3d1b190c2670d2c73af33c0a104b78f52ff0c0ff802604af0b03cd273d03666547aef0'
    wechat_appmsg_token = '994_p9KdAkZM2FDJu7sEKyzD3SE9T1weJADPi394yQ~~&x5=0'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = [
        # xiaohan wechat subscription json format home page.
        'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MjEyODU2MA==&f=json&offset=0&count=10&is_ok=1&scene=124&uin=MTUyNzUyMTA3Mw%3D%3D&key=' + wechat_key + '&pass_ticket=K9t7oVL4QBgxPtPRwoUk5g2YTodNqOatojRvwwPSry%2FiDAqqGcW2R5WMIh2MuPzM&wxtoken=&appmsg_token='+ wechat_appmsg_token +'&f=json',
        # before 41 episode, 42 episode is deleted.
        'http://mp.weixin.qq.com/s?__biz=MjM5MjEyODU2MA==&amp;mid=2651599455&amp;idx=1&amp;sn=f91bd3a391d41cdc53689fc0deefeb36&amp;chksm=bd5399008a24101608d40911744d61596f8afb97a05dd2e9c188d12eb95b0275cbff42ceb5cb#rd'
    ]
    parser_classes = [
        CardStyleParser,
        BoxStyleParser,
        TextStyleParser 
    ]
    def __first_page_url(self, response):
        raw = response.body_as_unicode()
        if raw.startswith('{'):
            rest_response = json.loads(raw)
            self.logger.debug('json response: %s', rest_response)
            if rest_response['errmsg'] == 'no session':
                self.logger.error('session expired.')
                return
            msglist = json.loads(rest_response['general_msg_list'])
            for msg in msglist['list']:
                title = msg['app_msg_ext_info']['title']
                url = msg['app_msg_ext_info']['content_url']
                if title.find('表白墙') > -1:
                    self.logger.debug('first page tilte: [%s] url: [%s]', title, url)
                    return url
        return None

    def parse(self, response):
        first_page_url = self.__first_page_url(response)
        if first_page_url is not None:
            yield response.follow(first_page_url, callback=self.parse)
        else:
            for clazz in self.parser_classes:
                parser = clazz(response)
                if parser.ismatched():
                    raw_intro = response.xpath('//script[contains(., "msg_title")]').extract_first()
                    intro = dict(re.compile(r'var\s+(msg.+|ct)\s+=\s+"(.+?)";').findall(raw_intro))
                    self.logger.debug('intro data: %s', intro)
                    for result in parser.extract():
                        result['subject'] = intro['msg_desc']
                        result['publishTime'] = int(intro['ct']) * 1000
                        yield result
                    if not parser.isexcepted():
                        self.logger.error('excepted %d items, but %d crawled', parser.excepted_count(), parser.parsed_count())
                        self.logger.error("spider is not complete while parsing the content of url: [%s].", response.url)
                        return

            next_link = response.css('a[href*="//mp.weixin.qq.com/s?__biz=MjM5MjEyODU2MA=="]::attr(href)').extract_first()
            
            if next_link is not None:
                time.sleep(1)
                yield response.follow(next_link, callback=self.parse)
        
        
