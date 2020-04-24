import scrapy

from ..items import SouqItem


class Gaming(scrapy.Spider):
    name = "gaming"
    page_number = 2
    start_urls = [
        'https://egypt.souq.com/eg-en/games-console/l/?ref=nav&section=2&page=1'
    ]

    def parse(self, response):
        product_name = []
        items = SouqItem()
        name = response.xpath("//h6[@class='title itemTitle']//text()").extract()
        for n in name:
            x = n.strip()
            product_name.append(x)
        price = response.xpath("//span[@class='itemPrice']/text()").extract()
        imageLink = response.xpath("//img[@class='img-size-medium lazy-loaded']/@src").extract()
        link = response.xpath("//a[@class='itemLink block sPrimaryLink']/@href").extract()

        items['name'] = product_name
        items['price'] = price
        items['imageLink'] = imageLink
        items['link'] = link

        yield items


        
        next_page = 'https://egypt.souq.com/eg-en/games-console/l/?ref=nav&section=2&page='+ str(Gaming.page_number)+'/'
            
        if Gaming.page_number < 4:
            Gaming.page_number += 1
            yield response.follow(next_page, callback=self.parse)
      

            

        # following_link
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

        # pagination

