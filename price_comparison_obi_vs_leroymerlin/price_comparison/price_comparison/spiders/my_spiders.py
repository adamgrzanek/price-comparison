# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
import scrapy


#from .ag_2 import obi_search, lm_search

# searching
with open('search_phrase.txt', 'r',  encoding='utf8') as f:
    obi = f.readline().rstrip()
    lm = f.readline()


class Spider_OBI(scrapy.Spider):

    name = 'items_OBI'
    start_urls = [
        f"https://www.obi.pl/search/{obi}/"
        #f"https://www.obi.pl/search/{obi_search}/"
        ]


    def parse(self, response):
        counter = 1
        output_obi = {}
        product_name = response.css('.description p::text').extract()
        product_price = response.css('.price span::text').extract()

        for n, p in zip(product_name, product_price):
            if counter == 11:
                break
            counter += 1
            output_obi[n] = p

        yield output_obi


class Spider_LM(scrapy.Spider):
    counter = 1
    name = 'items_LM'
    start_urls = [
        f'https://www.leroymerlin.pl/szukaj.html?q={lm}&sprawdz=true'
        #f'https://www.leroymerlin.pl/szukaj.html?q={lm_search}&sprawdz=true'
        ]

    def parse(self, response):
        counter = 1
        output_lm = {}
        product_name = response.css('#product-listing .title::text').extract()
        product_price_int = response.css('.integer::text').extract()
        product_price_frac = response.css('.fractional::text').extract()
        product_price_pf = response.css('.postfix::text').extract()
        product_price_unit = response.css('.unit::text').extract()

        for n, p, f, pf, u in zip(product_name, product_price_int, product_price_frac, product_price_pf, product_price_unit):
            n = n.replace('\n', '').replace('\t', '')
            if counter == 11:
                break
            counter += 1
            output_lm[n] = p+f+pf+u

        yield output_lm


from scrapy import cmdline
#cmdline.execute("scrapy crawl items_OBI -o obi.json".split())
#cmdline.execute("scrapy crawl items_LM -o lm.json".split())


# setings to save obi results in json file
process = CrawlerProcess(settings={
    "FEEDS": {
        "obi.json": {"format": "json"},
    },
})

process.crawl(Spider_OBI)


# setings to save leroy merlin results in json file
process = CrawlerProcess(settings={
    "FEEDS": {
        "lm.json": {"format": "json"},
    },
})

process.crawl(Spider_LM)
process.start()
