# -*- coding: utf-8 -*-
import scrapy
from SMUCrawler.items import SmucrawlerItem


class SemSpider(scrapy.Spider):
    name = 'sem'
    start_urls = [
        'http://sem.shmtu.edu.cn/page1.asp?Page=5&classid1=66&classid2=120'
        # 'http://sem.shmtu.edu.cn/page1.asp?Page=4&classid1=66&classid2=68',
        # 'http://sem.shmtu.edu.cn/page1.asp?classid1=66&classid2=67'
    ]
    handle_httpstatus_list = [301, 302]

    def parse(self, response):
        print(response.css('div.txt_list>table').extract())
        news_contents = response.css('div.txt_list>table')
        for news_content in news_contents:
            item = SmucrawlerItem()
            item['title'] = news_content.css('a::text').extract_first()
            item['date'] = news_content.css('td>div::text').extract_first()
            url = news_content.css('a::attr("href")').extract_first()
            item['url'] = response.urljoin(url)
            # try:
            #     scrapy.Request(url=url, meta={'item': item}, callback=self.inner_parse)
            # except:
            #     scrapy.Request(url=url, meta={'item': item}, callback=self.inner_parse)
            yield item
        next_page = response.css(
            'div.txt_body > div.txt_list > table:nth-child(11) > tbody > tr > td > div > a:nth-child(3)::attr("href")'
        ).extract_first()
        url = response.urljoin(next_page)
        yield scrapy.Request(
            url=url, callback=self.parse
        )

    @staticmethod
    def inner_parse(response):
        item = response.meta['item']
        item['main'] = response.css('.txt_main').extract_first()
        return item
