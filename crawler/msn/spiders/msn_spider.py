import scrapy
from urllib.parse import unquote
from ..items import NewsItem
import os

class MSNSpider(scrapy.Spider):
    name = "msn"
    allowed_domains = ["msn.com"]

    #start_urls = ["https://www.msn.com/en-us/sports/football_nfl/pittsburgh-steelers-well-represented-in-the-top-10-of-the-nfl's-top-100-teams/ar-BBWRHuM?ocid=chopendata"]
    #start_urls = ["file:D:\Repo\MIND\crawler\\test_sample\BBWRHuM.html"]
    start_urls = ["https://assets.msn.com/labs/mind/BBWRHuM.html"]
    
    """
    def parse(self, response):
        print(response)
        item = NewsItem()
        item['body'] = response.css('.articlecontent p::text, \
                                         .articlecontent p a::text, \
                                         .articlecontent blockquote::text, \
                                         .articlecontent blockquote a::text').getall()
        yield item

    """
    def parse(self, response):

        url = unquote(response.url)
        item = NewsItem()
        # parse nid, vert and subvert
        nid_type = self.parse_vert_subvert_nid_from_url(item, url)

        # parse title from response
        self.parse_title(response, item)

        # parse body from response
        self.parse_body(response, item, nid_type)

        yield item

    def parse_vert_subvert_nid_from_url(self, item, url):
        if 'refurl' not in url:
            url = url.split("/")[4:]
        else:
            url = url.split("/")[5:]
        item['vert'], item['subvert'] = url[:2]
        nid = url[-1]
        item['nid'] = nid.split('?')[0].split('-')[-1]
        return nid.split('?')[0].split('-')[0]

    def parse_title(self, response, item):
        try:
            item['title'] = response.xpath('//title/text()')[0].extract()
        except:
            url = response.url
            if 'refurl' not in url:
                url = url.split("/")[4:]
            else:
                url = url.split("/")[5:]
            item['title'] = ' '.join(url[2:-1]).replace('-', ' ')

    def parse_body(self, response, item, nid_type):

        # if metadate contains description take it as the first sentence
        # body_desc = response.xpath('//meta[@name="description"]/@content')[0].extract()

        # type1: ar-nid
        body = response.xpath('//div[@class="richtext"]//p/text() | \
                              //div[@class="richtext"]//a/text() | \
                              //div[@class="richtext"]//h2/text() | \
                              //div[@class="richtext"]//span/text()[not(ancestor::span[@class="caption truncate"] or ancestor::div[@class="xnetvidplayer "])]').getall()

        # type2: ss
        if body == [] and nid_type == 'ss':
            body = response.xpath('//div[@class="gallery-caption-text"]//text()')

        # type3: vi
        if body == [] and nid_type == 'video-description':
            body = response.xpath('//div[@class="video-description"]//text()')

        item['body'] = body
        

<<<<<<< HEAD
        yield item
    
=======
         
>>>>>>> master
        