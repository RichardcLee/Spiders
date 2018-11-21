# -*- coding: utf-8 -*-
import logging

# Scrapy settings for coolscrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'coolscrapy'

SPIDER_MODULES = ['coolscrapy.spiders']
NEWSPIDER_MODULE = 'coolscrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'coolscrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'huxiu_analyzer_wcy_id=fbpzagzqvhyo6pabhlo; gr_user_id=b5751c99-5117-42b1-be2b-df8b2445cc73;\
     b6a739d69e7ea5b6_gr_last_sent_sid_with_cs1=903653e0-93ce-495b-bc90-d881a313ace1; b6a739d69e7ea5b6\
     _gr_last_sent_cs1=0; Hm_lvt_324368ef52596457d064ca5db8c6618e=1523435680,1524401717,1524451986;\
      screen=%7B%22w%22%3A1280%2C%22h%22%3A720%2C%22d%22%3A1.5%7D; _ga=GA1.2.1871690301.1523435684;\
       _gid=GA1.2.1835743616.1524401717; aliyungf_tc=AQAAACd/Hwz/xwgAD+MGcM9JsDpyrjlL; SERVERID=03a0\
       7aad3597ca2bb83bc3f5ca3decf7|1524451986|1524451983; b6a739d69e7ea5b6_gr_session_id=903653e0-93ce-495b-bc\
       90-d881a313ace1; Hm_lpvt_324368ef52596457d064ca5db8c6618e=1524451986; b6a739d69e7ea5b6_gr_cs1=0',
    'Host': 'www.huxiu.com',
    'Referer': 'https://www.baidu.com/link?url=8UtvQ0J-l4GioVBLO4MRL6C7PQCoIiY_J6xKUtVPXf\
    _&wd=&eqid=b8ad47fe00013744000000035add4a8c',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'coolscrapy.middlewares.CoolscrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'coolscrapy.middlewares.CoolscrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'coolscrapy.pipelines.CoolscrapyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

