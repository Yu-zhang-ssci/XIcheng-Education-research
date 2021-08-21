import scrapy 
import re
import math
class DistrictSpider(scrapy.Spider):
    name="District"
    def start_requests(self):
        urls='http://www.ysxiao.cn/c/202008/38679.html'
        yield scrapy.Request(url=urls,callback=self.parse)
    def parse(self,response):
        Dlist=response.css('table').css('td::text').getall()
        Districts=[Dlist[m] for m in range(len(Dlist)) if m%2==1]
        hrefs=response.css('table').css('a::attr(href)').getall()
        DistrictDict={}
        for id,district in enumerate(Districts):
            result=response.follow(hrefs[id],callback=self.parse_district)
            result.cb_kwargs['district']=district
            yield result
        #yield DistrictDict
    def parse_district(self,response,district):
        schoollist=response.css('table').css('td::text').getall()
        schools=[schoollist[m] for m in range(len(schoollist)) if m%2==1]
        hrefs=response.css('table').css('a::attr(href)').getall()
        hrefdict=[]
        for href in hrefs:
             result=response.follow(href,callback=self.parse_school)
             result.cb_kwargs['district']=district
             yield result
        #return  {'http':hrefs}
    def parse_school(self,response,district):
        title=response.css('div.content h2::text').getall()[0]
        year=title[:4]
        region=title[5:8]
        school=title[8:-6]
        addresslist=response.css('div.content p::text').getall()[1:-4]
        neighborlist=[]
        for address in addresslist:
            var=address.split('：')
            print (var)
            for word in var:
                if '居委会' in word:
                    neighborlist.append(word)
        print ({'year':year,'region':region,'district':district,'school':school,'area':addresslist,'committee':neighborlist    })
        yield {'year':year,'region':region,'district':district,'school':school,'area':addresslist,'committee':neighborlist}
