# -*- coding: utf-8 -*-

# Define here the parser for your scraped items
import logging
import re

class Parser(object):
    response = None
    logging = None

    @property
    def logger(self):
        logger = logging.getLogger(__name__)
        return logging.LoggerAdapter(logger, {'parser': self})

    def __init__(self, response):
        self.response = response
    def ismatched(self):
        return False
    def extract(self):
        yield None
    def parsed_count(self):
        return 0
    def excepted_count(self):
        return 0
    def isexcepted(self):
        return False

class CardStyleParser(Parser):
    letters_raw = None
    count = 0
    letter_flags = None
    def __init__(self, response=None):
        super().__init__(response)
        self.letter_flags = response.css('p[style*="background-color: rgb(251, 139, 173);"] ::text')
        self.letters_raw = self.response.css('section[style^="padding: 20px 24px 18px 50px;"]')

    def ismatched(self):
        title_raw = self.response.css('title::text')
        return (self.letters_raw is not None) and len(self.letters_raw) > 0 and (title_raw is not None)
    def extract(self):
        self.count = 0
        if self.ismatched():
            title_raw = self.response.css('title::text')
            for letter_raw in self.letters_raw:
                extracted_letter_address = letter_raw.css('strong ::text').extract()
                address_raw = ''.join(extracted_letter_address)
                self.logger.debug('address data: %s', extracted_letter_address)
                extracted_letter_body = letter_raw.css('section ::text').extract()
                self.logger.debug('letter data: %s', extracted_letter_body)
                self.count += 1
                yield {
                    'ep': title_raw.extract_first().strip(),
                    'to': (address_raw[address_raw.find('：') + 1:address_raw.rfind('From：')]).strip(),
                    'from': (address_raw[address_raw.rfind('：') + 1:]).strip(),
                    'content': (''.join(set(extracted_letter_body).difference(set(extracted_letter_address)))).strip(),
                    'link': self.response.url
                }
    def parsed_count(self):
        return self.count
    def excepted_count(self):
        return len(self.letter_flags)
    def isexcepted(self):
        return self.count == self.excepted_count()

class BoxStyleParser(Parser):
    letters_raw = None
    page_text = None
    matching_patterns = [
        r'^(离我而去.+?)[，,]([\s\S]+)[—-]+([\s\S]+?)$',
        r'^(才不告诉你.+?)[，,]([\s\S]+)[—-]+([\s\S]+?)$',
        r'^(我.+?)[，,]([\s\S]+)[—-]+([\s\S]+?)$',
        r'^(.+?)[，,]([\s\S]+?)，爱你（([\s\S]+)）$',
        r'^([^我你]+?)[，,]([\s\S]+)[—-]+([\s\S]+?)$',
        r'^(.{1,3})(我[\s\S]+)[—-]+([\s\S]+?)$',
        r'^(.{1,3})(你[\s\S]+)[—-]+([\s\S]+?)$',
        r'^(.{1,3})(亲爱的[\s\S]+)[—-]+([\s\S]+?)$',
        r'^(.{1,3})(喜欢[\s\S]+)[—-]+([\s\S]+?)$',
        r'^(.{1,3})([\s\S]+)[—-]+([\s\S]+?)$',
        r'^(.{1,3})(2016\.4\.3[\s\S]+)[—-]+([\s\S]+?)$',
        r'^([^我你]+?)[~！]([\s\S]+)[—-]+([\s\S]+?)$',
    ]
    count = 0
    def __init__(self, response=None):
        super().__init__(response)
        self.letters_raw = self.response.css('*[style*="padding: 28px 16px 16px;"]')
        self.page_text = ''.join(self.response.css('#js_content ::text').extract())

    def ismatched(self):
        return (self.letters_raw is not None) and len(self.letters_raw) > 0
    def __match(self, letter_text):
        result = None
        for pattern in self.matching_patterns:
            self.logger.debug('matching pattern: /%s/ ', pattern)
            result = re.match(pattern, letter_text)
            self.logger.debug('matched result: %s', result)
            if (result is not None):
                break
        return result

    def __try_to_match(self, letter_text):
        result = self.__match(letter_text)
        if result is None:
            self.logger.warning('rematch again with [--spider_nodata] sender.')
            result = self.__match(letter_text + '--spider_nodata')
        return result

    def extract(self):
        self.count = 0
        if self.ismatched():
            title_raw = self.response.css('title::text')
            for letter_raw in self.letters_raw:
                letter_text = ''.join(letter_raw.css('::text').extract())
                self.logger.debug('letter text: %s', letter_text)
                result = self.__try_to_match(letter_text)
                self.logger.debug('letter data: %s', result.groups())
                if (result is not None):
                    content = result.group(2).strip()
                    while content.endswith('-'):
                        content = content[:content.rfind('-')]
                    while content.endswith('—'):
                        content = content[:content.rfind('—')]
                    self.count += 1
                    yield { 
                        'ep': title_raw.extract_first().strip(),
                        'to': result.group(1).strip(),
                        'from': result.group(3).strip(),
                        'content': content,
                        'link': self.response.url
                    }
                else:
                    self.logger.warning('does not match [%s]', letter_raw)
    def parsed_count(self):
        return self.count
    def excepted_count(self):
        return len(re.findall(r'表白\d+', self.page_text))
    def isexcepted(self):
        return self.count == self.excepted_count()

class TextStyleParser(Parser):
    count = 0
    letter_flags = None
    letters_raw = None
    def __init__(self, response=None):
        super().__init__(response)
        self.letter_flags = self.response.css('span[style*="background-color: rgb(255, 127, 170);"] ::text')
    def ismatched(self):
        letters_a = self.response.css('section[style^="padding: 20px 24px 18px 50px;"]')
        letters_b = self.response.css('section[style^="padding: 28px 16px 16px;"]')
        return len(letters_a) == 0 and len(letters_b) == 0
    def extract(self):
        self.count = 0
        if self.ismatched():
            title_raw = self.response.css('title::text')
            page_text = ''.join(self.response.css('#js_content ::text').extract())
            letters_text = page_text[page_text.find('表白1'):page_text.rfind('PS')]
            letters_text = letters_text + '表白99'
            self.letters_raw = re.split(r'表白\d{1,2}', letters_text)
            self.logger.info('%d items will be test to match', len(self.letters_raw))
            for letter_raw in self.letters_raw:
                self.logger.debug('letter data: %s', letter_raw)
                result = re.match(r'^([\s\S]+?)：([\s\S]+)[—-]+([\s\S]*?)$', letter_raw)
                if (result is not None):
                    content = result.group(2).strip()
                    while content.endswith('-'):
                        content = content[:content.rfind('-')]
                    while content.endswith('—'):
                        content = content[:content.rfind('—')]
                    self.count += 1
                    yield { 
                        'ep': title_raw.extract_first().strip(),
                        'to': result.group(1).strip(),
                        'from': result.group(3).strip(),
                        'content': content,
                        'link': self.response.url
                    }
                else:
                    self.logger.warning('does not match [%s]', letter_raw)
    def parsed_count(self):
        return self.count
    def excepted_count(self):
        return len(self.letter_flags)
    def isexcepted(self):
        return self.count == self.excepted_count()
