import scrapy
from urllib.parse import unquote
from ..items import NewsItem
import os
import json

class MSNSpider(scrapy.Spider):
    name = "msn"
    allowed_domains = ["msn.com"]

    start_urls = []
    with open(os.environ["MIND_NEWS_PATH"], 'r') as f:
        for l in f:
            _, _, _, _, _, url, _, _ = l.strip('\n').split('\t')
            start_urls.append(url)

    # start_urls = [
    #     # ss
    #     "https://mind201910small.blob.core.windows.net/archive/AAGH0ET.html",
    #     # ar
    #     "https://mind201910small.blob.core.windows.net/archive/AABmf2I.html",
    #     # vi
    #     "https://mind201910small.blob.core.windows.net/archive/AAI33em.html"
    # ]

    def __init__(self):
        with open('./doc_type.json', 'r') as f:
            self.doc_type = json.load(f)

        super().__init__()

    def parse(self, response):

        url = unquote(response.url)
        item = NewsItem()
        # parse nid, vert and subvert
        nid_type = self.parse_nid_from_url(item, url)

        # parse body from response
        self.parse_body(response, item, nid_type)

        yield item

    def parse_nid_from_url(self, item, url):
        item['nid'] = url.split('/')[-1].split('.')[-2]
        return self.doc_type[item['nid']]

    def parse_body(self, response, item, nid_type):

        # if metadate contains description take it as the first sentence
        # body_desc = response.xpath('//meta[@name="description"]/@content')[0].extract()

        # type1: ar-nid
        if nid_tyep == 'ar':
            body = response.xpath('//p/text()').getall()

        # type2: ss
        if body == [] and nid_type == 'ss':
            body = response.xpath('//div[@class="gallery-caption-text"]//text()').getall()

        # type3: vi
        if body == [] and nid_type == 'vi':
            body = response.xpath('//div[@class="video-description"]//text()').getall()

        item['body'] = body
        

         
        