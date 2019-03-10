import scrapy

class MAZhiZhu(scrapy.Spider):
    name = "MAZhiZhu"

    def start_requests(self):
        for auth in ['gao', 'gao2', 'he', 'gallos', 'fefferman', 'havlin', 'cohen', 'lieberthal']:
            url = 'file:///ma/{}.htm'.format(auth)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for entry in response.xpath('//a[@class="title au-target"]'):
            link = entry.xpath('@href').extract_first()
            title = entry.xpath('text()').extract()[1].strip()
            yield {'paper': link, 'title': title}

    def parse2(self, response):
        for entry in response.css('.paper'):
            link = entry.css('div a::attr(href)').extract_first()
            if link is None:
                yield ('missed {0},{1}'.format(entry.css('div a::text').extract_first(), response.url))
                continue
            else:
                yield scrapy.Request(base+link,callback=self.parse_next)

    def parse_next(self, response):
        authors = response.css('div.gsc_vcd_value ::text').extract_first()
        title = response.css('a.gsc_vcd_title_link ::text').extract_first()
        yield {'url': response.url, 'auths':authors, 'title': title}
