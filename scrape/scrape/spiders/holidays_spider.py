import scrapy, re
from scrape.items import HolidayItem

class HolidaysSpider(scrapy.Spider):
    name = "holidays"
    allowed_domains = ["holidayinsights.com"]
    start_url = "http://www.holidayinsights.com/moreholidays/"
    start_urls = [
        start_url
    ]

    def full_url(self, link):
        return "%s%s" % (self.start_url, link)

    def parse(self, response):
        # Find the months to crawl
        for sel in response.xpath('//a'):
            text = re.sub('<[^<]+?>', '', sel.extract())
            link = sel.xpath('@href').extract()[0]
            # e.g. title = January, link = january.htm
            if ("%s.htm" % text.lower()) == link:
                url = self.full_url(link)
                self.urls_to_months[url] = text
                yield scrapy.Request(url, callback=self.parse_month)
                
    def parse_month(self, response):
        # Find days to crawl
        month = self.urls_to_months[response.url]
        for sel in response.xpath('//p'):
            link_sels = sel.xpath('a')
            if not link_sels or len(link_sels) != 1:
                continue
            link_sel  = link_sels[0]
            text = re.sub('<[^<]+?>', '', link_sel.extract())
            text = re.sub('\n', '', text)
            text = re.sub('\s+', ' ', text)
            link = link_sel.xpath('@href').extract()[0]
            url = self.full_url(link)
            num_text = re.sub('<.*', '', sel.extract())
            num_text = re.sub('\D', '', num_text)
            num_text = re.sub('\s+', '', num_text)
            if text.lower().endswith('day') and url.find(month):
                day = int(num_text)
                item = HolidayItem(title=text, day=day, month=month, url=url)
                yield item
