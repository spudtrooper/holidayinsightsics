# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HolidayItem(scrapy.Item):
    # http://www.holidayinsights.com/other/newyears.htm
    url = scrapy.Field()
    title = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
