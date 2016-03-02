# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from piccrawler.items import PiccrawlerItem
import re
import urllib

class DoubanSpider(Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = []

    def start_requests(self):
        file_object = open('movie_name.txt','r')

        try:
            url_head = "http://movie.douban.com/subject_search?search_text="
            for line in file_object: 
                # print "查看文件内容:", line
                self.start_urls.append(url_head + line)
            
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        finally:
            file_object.close()
            # years_object.close()

    def parse(self, response):
        #open("test.html",'wb').write(response.body)
        hxs = HtmlXPathSelector(response)
        movie_link = hxs.select('//*[@id="content"]/div/div[1]/div[2]/table[1]/tr/td[1]/a/@href').extract()
        # print "获取第一个搜索结果链接:", movie_link[0]
        if movie_link:
            yield Request(movie_link[0],callback=self.parse_item)
        
        
    def parse_item(self,response):
        hxs = HtmlXPathSelector(response)
        movie_picture = hxs.select('//*[@id="mainpic"]/a/img/@src').extract()

        item = PiccrawlerItem()
        item['movie_picture'] = ''.join(movie_picture).strip()

        #用来给爬到的图片命令的，这个文件里只有一行数据，因为我会在我的main.py文件中调用scrapy爬虫，会在main.py中不断更新这个文件
        movie_id_file = open('movie_id.txt','r')
        try:
            for line in movie_id_file:
                item['movie_id'] = line.strip()
                # print "图片id:", line.strip()
                if movie_picture:
                    urllib.urlretrieve(movie_picture[0].strip(),'pictures/' + line.strip() + '.jpg')
        finally:
            movie_id_file.close()


        yield item