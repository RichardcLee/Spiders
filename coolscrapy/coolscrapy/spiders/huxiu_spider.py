# -*- coding: utf-8 -*-
import scrapy
from ..items import HuXiuItem, ArticleItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError


class HuxiuSpiderSpider(scrapy.Spider):
    name = 'huxiu_spider'
    allowed_domains = ['www.huxiu.com']
    start_urls = ['https://www.huxiu.com/']

    def parse(self, response):
        for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt index-article-list-yh"]'):
            item = HuXiuItem()
            item['title'] = sel.xpath('h2/a/text()').extract_first()
            url = sel.xpath('h2/a/@href').extract_first()
            item['link'] = response.urljoin(url)
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()').extract_first()
            yield item
            # print(item)
            yield scrapy.Request(item['link'], callback=self.parse_article, errback=self.errback_httpbin)

    def parse_article(self, response):
        item = ArticleItem()
        item['title'] = response.css("h1.t-h1::text").extract_first()
        item['author'] = response.css("div.article-author span.author-name a::text").extract_first()
        item['post_time'] = response.css("div.column-link-box span.article-time.pull-left::text").extract_first()
        item['content'] = response.css("div.article-content-wrap p::text").extract()
        return item

    '''
        request错误、异常回调函数
    '''
    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
