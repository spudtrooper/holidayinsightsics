# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from datetime import date

class ICal(object):

    MONTHS_TO_NUMS = { 
        "January" : 1,
        "February" : 2,
        "March" : 3,
        "April" : 4,
        "May" : 5,
        "June" : 6,
        "July" : 7,
        "August" : 8,
        "September" : 9,
        "October" : 10,
        "November" : 11,
        "December" : 12
    }

    def header(self,locations=None):
        res = ''
        res += "BEGIN:VCALENDAR\r\n"
        res += "VERSION:2.0\r\n"
        res += "PRODID:-//jeffpalm/holidayinsights//NONSGML v1.0//EN\r\n"
        name = 'Holiday Insights'        
        res += "X-WR-CALNAME:%s\r\n" % (name)
        return res

    def footer(self):
        res = ''
        res += "END:VCALENDAR\r\n"
        return res

    def pad(self, n):
        if (n < 10):
            return '0%d' % (n)
        return '%d' % (n)

    def getDate(self, item):
        year = date.today().year
        day = self.pad(item['day'])
        month = self.pad(self.MONTHS_TO_NUMS[item['month']])
        return ''.join(map(lambda s:str(s), [year,month,day]))

    def toEvent(self, item, offset=0):
        """
        @param item
        @param offset number hours to pad dates
        """
        res = ''
        res += "BEGIN:VEVENT\r\n"
        title = item['title']
        uid = re.sub('\s', '', title)
        #res += "UID:%s\r\n" % (uid)
        date = self.getDate(item)
        res += "DTSTART:%s\r\n" % (date)
        res += "DTEND:%s\r\n" % (date)
        summary = title
        res += "SUMMARY:%s\r\n" % (summary)
        res += "LOCATION:%s\r\n" % (item['url'])
        res += "END:VEVENT\r\n"
        return res


class ICalPipeline(object):
    """Converts items to ical entries."""

    def open_spider(self, spider):
        self.ical = ICal()
        self.outfile = open('holidayinsights.ics', 'wb')
        self.output(self.ical.header())

    def output(self, string):
        self.outfile.write(string)

    def close_spider(self, spider):
        self.output(self.ical.footer())
        self.outfile.close()

    def process_item(self, item, spider):
        event = self.ical.toEvent(item)
        self.output(event)
        return item
