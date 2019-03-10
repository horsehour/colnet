import scrapy

class ZhiZhu(scrapy.Spider):
    name = "ZhiZhu"

    def start_requests(self):
        for auth in ['gao', 'he', 'gallos', 'fefferman', 'havlin', 'cohen', 'blumenfeld']:
            url = 'file:///coauth/{}.htm'.format(auth)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base = 'https://scholar.google.com'
        for entry in response.css('.gsc_a_t'):
            link = entry.css('td a::attr(data-href)').extract_first()
            if link is None:            	
                yield ('missed {0},{1}'.format(entry.css('td a::text').extract_first(), response.url))
                continue
            else:
                yield scrapy.Request(base+link,callback=self.parse_next)

    def parse_next(self, response):
        authors = response.css('div.gsc_vcd_value ::text').extract_first()
        title = response.css('a.gsc_vcd_title_link ::text').extract_first()
        yield {'url': response.url, 'auths':authors, 'title': title}
