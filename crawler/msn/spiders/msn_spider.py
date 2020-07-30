import scrapy
from urllib.parse import unquote
from ..items import NewsItem
import os

class MSNSpider(scrapy.Spider):
    name = "msn"
    allowed_domains = ["msn.com"]

    start_urls = []
    with open(os.environ["MIND_NEWS_PATH"], 'r') as f:
        for l in f:
            _, _, _, _, _, url, _, _ = l.strip('\n').split('\t')
            start_urls.append(url)
    #start_urls = start_urls[:1000]
    #start_urls = ["https://www.msn.com/en-us/news/world/chile-three-die-in-supermarket-fire-amid-protests/ar-AAJ43pw?ocid=chopendata"]

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
        

         
        