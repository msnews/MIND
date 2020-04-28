import scrapy
from urllib.parse import unquote
from ..items import NewsItem
import os

class MSNSpider(scrapy.Spider):
    name = "msn"
    allowed_domains = ["msn.com"]

    start_urls = ["https://www.msn.com/en-us/sports/football_nfl/pittsburgh-steelers-well-represented-in-the-top-10-of-the-nfl's-top-100-teams/ar-BBWRHuM?ocid=chopendata"]

    def parse(self, response):

        url = unquote(response.url)
        item = NewsItem()
        try:
            if 'refurl' not in url:
                item['vert'], item['subvert'], title, nid = url.split("/")[4:8]
                item['title'] = title.replace('-', ' ')
                item['nid'] = nid.split('?')[0]
                item['body'] = response.css('.articlecontent p::text, \
                                         .articlecontent p a::text, \
                                         .articlecontent blockquote::text, \
                                         .articlecontent blockquote a::text').getall()
            else:
                item['vert'], item['subvert'], title, nid = url.split("/")[5:9]
                item['title'] = title.replace('-', ' ')
                item['nid'] = nid.split('?')[0]
                item['body'] = response.css('.articlecontent p::text, \
                                         .articlecontent p a::text, \
                                         .articlecontent blockquote::text, \
                                         .articlecontent blockquote a::text').getall()
        except Exception as e:
            print(e, url)


        yield item
         
        