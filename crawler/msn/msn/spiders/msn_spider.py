import scrapy
from urllib.parse import unquote
from ..items import NewsItem
import os

class MSNSpider(scrapy.Spider):
    name = "msn"
    allowed_domains = ["msn.com"]

    start_urls = []
    # with open("/home/v-jinyi/data/MIND/sam/train/news.tsv", 'r') as f:
    #     for l in f:
    #         _, _, _, _, _, url, _ = l.strip('\n').split('\t')
    #         start_urls.append(url)
    start_urls = ["https://www.msn.com/en-us/health/weightloss/if-you-have-a-slow-metabolism,-here-are-5-doctor-approved-ways-to-burn-belly-fat/ss-AAGiUfU?ocid=chopendata"]

    def parse(self, response):

        url = unquote(response.url)
        item = NewsItem()
        # parse title, nid, vert and subvert
        self.parse_vert_subvert_tile_nid(item, url)

        # parse body from response
        self.parse_body(response, item)

        yield item

    def parse_vert_subvert_tile_nid(self, item, url):
        if 'refurl' not in url:
            url = url.split("/")[4:]
            item['vert'], item['subvert'], title, nid = url
        else:
            url = url.split("/")[4:]
            item['vert'], item['subvert'], title, nid = url
        item['vert'], item['subvert'] = url[:2]
        title = ''.join(url[2:-1])
        nid = url[-1]
        item['title'] = title.replace('-', ' ')
        item['nid'] = nid.split('?')[0].split('-')[-1]

    def parse_body(self, response, item):
        body1 = response.css('.articlecontent p::text, \
                                    .articlecontent p a::text, \
                                    .articlecontent blockquote::text, \
                                    .articlecontent blockquote a::text').getall()

       
        body2 = response.css('.richtext p::text').getall()

        item['body'] = body1 + body2
        

         
        