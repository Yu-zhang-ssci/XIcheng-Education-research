import scrapy 
import re

class LianJia(scrapy.Spider):
    name="LianJia"
    def start_requests(self):
        urls=['https://bj.lianjia.com/xiaoqu/xicheng/pg%d/'%i for i in range(31,43)]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self,response):
        areainfos=response.css('div.info')
        priceinfos=response.css('div.totalPrice')
        for idx in range(len(areainfos)):
            name=areainfos[idx].css("a::text").getall()[0]
            price=priceinfos[idx].css("span::text").getall()[0]
            href=areainfos[idx].css("a::attr(href)").get()
            result=response.follow(href,callback=self.parse_detail)
            result.cb_kwargs['villagedict']={
                "name":name,'price':price
            }
            yield result 
    def parse_detail(self,response,villagedict):
        roomnum=response.css('body span.xiaoquInfoContent::text').getall()[-2]
        coord=response.css('body span.xiaoquInfoContent span::attr(xiaoqu)').getall()
        villagedict['roomnum']=roomnum
        villagedict['coord']=coord
        return villagedict  

