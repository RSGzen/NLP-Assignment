import scrapy
import logging
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider

class GamersnexusSpider(scrapy.Spider):
    name = "gamersnexus"
    allowed_domains = ["gamersnexus.net"]
    start_urls = ["https://gamersnexus.net/cat/gpus?page=0"]

    def __init__(self, *args, **kwargs):

        self.base_url = "https://gamersnexus.net"
        self.current_link_idx = 0
        self.downloaded_articles_num = 0

        logging.getLogger('scrapy').setLevel(logging.WARNING)

        super().__init__(*args, **kwargs)
    
    def parse(self, response):        
        page_links = ["https://gamersnexus.net/cat/gpus?page=1",
                      "https://gamersnexus.net/cat/gpus?page=2",
                      "https://gamersnexus.net/cat/gpus?page=3",
                      "https://gamersnexus.net/cat/gpus?page=4",
                      "https://gamersnexus.net/cat/cpus?page=0",
                      "https://gamersnexus.net/cat/cpus?page=1",
                      "https://gamersnexus.net/cat/cpus?page=2",
                      "https://gamersnexus.net/cat/cpus?page=3",
                      "https://gamersnexus.net/cat/cases?page=0",
                      "https://gamersnexus.net/cat/cases?page=1",
                      "https://gamersnexus.net/cat/cases?page=2",
                      "https://gamersnexus.net/cat/cases?page=3",
                      "https://gamersnexus.net/cat/coolers?page=0",
                      "https://gamersnexus.net/cat/coolers?page=1",
                      "https://gamersnexus.net/cat/coolers?page=2",]

        for link in response.css(".card-body a::attr(href)").getall():
            link = urljoin(self.base_url, link)
            print(f"Scraping article: {link}")
            yield scrapy.Request(link, callback=self.parse_text)
        
        yield scrapy.Request(page_links[self.current_link_idx], callback=self.parse)
        
        if self.current_link_idx < len(page_links):
            self.current_link_idx += 1
        else:
            CloseSpider(reason="Finished scraping all links")
    
    def parse_text(self, response):
        self.downloaded_articles_num += 1
        
        title = response.css("div.content h1::text").get()
        para = response.css("div.content p::text").getall()

        yield{
            "title": title,
            "paragraph": para
        }

        print(f"Donwloaded article no. {self.downloaded_articles_num}")