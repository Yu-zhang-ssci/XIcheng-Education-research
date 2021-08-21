import scrapy 
import re

class AnjuSpider(scrapy.Spider):
    name="Anjuke"
    def start_requests(self):
        urls=['https://beijing.anjuke.com/community/xicheng/p%d/'%i for i in range(1,49)]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self,response):
        for areainfo in response.css('div.li-itemmod'):
            name=areainfo.css("a.img::attr(alt)").get()
            address=areainfo.css("address::text").get().strip()
            price=areainfo.css("strong::text").get()
            coord=areainfo.css("p.bot-tag a::attr(href)").getall()[1]
            matchobj=re.search(r'l1=(.*)&l2=(.*)&l3=',coord,re.M|re.I)
            x=matchobj.group(1)
            y=matchobj.group(2)
            href=areainfo.css("a::attr(href)").get()
            result=response.follow(href,callback=self.parse_detail)
            result.cb_kwargs['villagedict']={
                "name":name,'address':address,'price':price,'x':x,'y':y
            }
            yield result 
        """
        page=response.url.split("/")[-2]
        filename='xicheng-%s.html'%page
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('Saved file %s'%filename)
        """
    def parse_detail(self,response,villagedict):
        roomnum=response.css('body div.basic-infos-box dd.other-dd::text').getall()[1]
        villagedict['roomnum']=roomnum
        return villagedict  

