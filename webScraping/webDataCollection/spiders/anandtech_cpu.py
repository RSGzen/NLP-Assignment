import scrapy
import logging
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider

class AnandtechSpider_CPU(scrapy.Spider):
    name = "anandtech_cpus"
    allowed_domains = ["www.anandtech.com"]
    start_urls = ["https://www.anandtech.com/tag/cpus"]

    def __init__(self, *args, **kwargs):

        self.base_url = "https://www.anandtech.com/tag/cpus"
        self.current_link_idx = 2
        self.downloaded_articles_num = 0
        self.PAGE_HARD_LIMIT = 40

        logging.getLogger('scrapy').setLevel(logging.WARNING)

        super().__init__(*args, **kwargs)
    
    def parse(self, response):        

        for link in response.xpath('//*[@class="cont_box1_pic pie"]/a/@href').extract():
            link = urljoin(self.base_url, link)
            print(f"Scraping article: {link}")
            yield scrapy.Request(link, callback=self.parse_text)
        
        page_link = self.base_url + r"/" + str(self.current_link_idx)
        print(f"Next page link: {page_link}")

        yield scrapy.Request(page_link, callback=self.parse)
        
        if self.current_link_idx < self.PAGE_HARD_LIMIT:
            self.current_link_idx += 1
        else:
            CloseSpider(reason="Finished scraping all links")
    
    def parse_text(self, response):
        self.downloaded_articles_num += 1
        
        title = response.css("div.blog_top_left h1::text").get()
        para = response.css("div.articleContent p::text").getall()

        yield{
            "title": title,
            "paragraph": para
        }

        print(f"Donwloaded article no. {self.downloaded_articles_num}")