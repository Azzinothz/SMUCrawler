# -*- coding: utf-8 -*-
import scrapy
from SMUCrawler.items import SmucrawlerItem

import re


class SemSpider(scrapy.Spider):
    name = 'SemNotice'
    current_page = 1
    start_urls = ['http://sem.shmtu.edu.cn/page1.asp?Page=4&classid1=66&classid2=68']
    handle_httpstatus_list = [301, 302]
    max_page = 1

    def parse(self, response):
        news_contents = response.css('div.txt_list>table')
        for news_content in news_contents:
            if news_content.css('table::attr("width")').extract_first() == '100%':
                item = SmucrawlerItem()
                item['title'] = news_content.css('a::text').extract_first()
                item['date'] = news_content.css('td>div::text').extract_first()
                url = news_content.css('a::attr("href")').extract_first()
                item['url'] = response.urljoin(url)
                item['category'] = '公告通知'
                yield scrapy.Request(url=item['url'], meta={"item": item}, callback=self.inner_parse)
            elif self.max_page == -1:
                raw_str = news_content.css('div::text').extract_first()
                self.max_page = int(re.search('.*分为(.*)页，.*', raw_str).group(1).strip(" "))
        if response.status == 200:
            if self.current_page != self.max_page:
                self.current_page += 1
        next_page = 'http://sem.shmtu.edu.cn/page1.asp?Page=' + str(self.current_page) + '&classid1=66&classid2=120'
        yield scrapy.Request(
            url=next_page, callback=self.parse
        )

    @staticmethod
    def inner_parse(response):
        item = response.meta["item"]
        item['main'] = response.css('.txt_main').extract_first()
        return item
