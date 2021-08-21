import scrapy 
import re
import math
class DistrictSpider(scrapy.Spider):
    name="School"
    def start_requests(self):
        starturl='http://xuexiao.51sxue.com/slist/?o=&t=2&areaCodeS=110102&level=&sp=&score=&order=&areaS=%CE%F7%B3%C7%C7%F8&searchKey=&page='
        for pageindex in range(1,8):
            url=starturl+'%d'%pageindex
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self,response):
        schoolnamelist=response.css('div.reply_box h3 a::attr(title)').getall()
        propertieslist=response.css('div.reply_box b::text').getall()
        scorelist=response.css('div.reply_box div.school_m_df img::attr(src)').getall()
        for i in range(len(schoolnamelist)):
            schooldict={}
            schooldict['name']=schoolnamelist[i]
            schooldict['area']=propertieslist[i*7]
            schooldict['level']=propertieslist[i*7+1]
            schooldict['type']=propertieslist[i*7+2]
            schooldict['class']=propertieslist[i*7+3]
            schooldict['comnum']=int(propertieslist[i*7+4])
            schooldict['address']=propertieslist[i*7+5]
            schooldict['telphone']=propertieslist[i*7+6]
            schooldict['score']=float(scorelist[i].split('/')[-1][:-4])
            yield schooldict
            
