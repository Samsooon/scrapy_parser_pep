import scrapy


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        links = response.xpath(
            '//a[@class="pep reference internal"]/@href'
        ).getall()
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        h1 = response.css('h1.page-title::text').get().split(' – ')

        yield {
            'number': int(h1[0][4:]),
            'name': h1[1],
            'status': response.css('abbr::text').get()
        }
