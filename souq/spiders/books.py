import scrapy
from bs4 import BeautifulSoup
import re
from souqar.items import SouqarItem


class BB(scrapy.Spider):
    name = "bb"

    start_urls = [
        'https://egypt.souq.com/eg-ar/shop-all-categories/c/?ref=nav'
    ]

    def __init__(self):
        self.declare_xpath()

    def declare_xpath(self):
        
        self.getAllCategriesXpath = "//*[@id='content-body']/div/div/div[2]/div/div[3]/div[2]/ul/li/a/@href"
        self.getAllProductsXpath = "//*[@id='content-body']/div[5]/div/div/div/div[2]/ul/li[1]/h6/a/@href"
        self.TitleXpath = "//h1/text()"
        self.CategoryCss = "h1+ span a+ a::text"
        self.PriceCss = ".is::text"
        self.DescriptionXpath = "//li[@class='level-1 clearfix']"
        self.ReviewsCss = "#reviews-list-id p::text"
        self.RateCss = ".rate-of-avg strong::text"
        self.ImagesCss = ".img-bucket img::attr(src)"

    def parse(self, response):
        for href in response.xpath(self.getAllCategriesXpath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url=url, callback=self.parse_category)

        # next_page = response.xpath("").extract_first()
        # if next_page is not None:
        #     url = response.urljoin(next_page)
        #     yield scrapy.Request(url, callback=self.parse_caregory, dont_filter=True)
    


    def parseText(self, x):
        soup = BeautifulSoup(x, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0", ' ', soup.get_text()).strip()


    def parse_category(self, response):
        item = SouqItem()

        Title = response.xpath(self.TitleXpath).get()

        Category = response.css(self.CategoryCss).get()

        Price = response.css(self.PriceCss).get()
        Price = self.parseText(Price)

        Description = response.xpath(self.TitleXpath).get()
        Description = self.parseText(Description)

        Reviews = response.css(self.ReviewsCss).extract()

        Rate = response.css(self.RateCss).get()
        Rate = self.parseText(Rate)

        Image_urls = response.css(self.ImagesCss).get()

        # Put each element into its item attribute.
        items['name'] = product_name
        items['price'] = price
        items['imageLink'] = imageLink
        items['link'] = link
        items['category'] = category
        return item


    def parseText(self, x):
        soup = BeautifulSoup(x, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0", ' ', soup.get_text()).strip()


