import scrapy
import re
import math
from urllib.parse import quote,unquote,urlencode
class UniqueLigandSpider(scrapy.Spider):
    name="pdbscrapy"
    def start_requests(self):
        with open('/Users/myxu/Desktop/Yu/scrapy/Beijingwest/Beijingwest/spiders/PDBID.list','r') as f:
            pdbidlist=[line.strip() for line in f.readlines()]
        times=math.ceil(len(pdbidlist)/25.0)
        searchdict={"query":{
                                "parameters":{"value":"9xim"},
                                "service":"text",
                                "type":"terminal","node_id":0
                            },
                    "return_type":"entry",
                    "request_options":{
                                            "scoring_strategy":"combined",
                                            "sort":[{"sort_by":"score","direction":"desc"}],
                                            "pager":{"start":0,"rows":100}
                                        },
                    "request_info":{"src":"ui","query_id":"3c659f470ace525c95777f74d89dbc7c"}
                    }
        for i in range(1):
            searchstr=','.join(pdbidlist[i:(i+1)*25])
            print (searchstr)
            searchdict["query"]["parameters"]["value"]=searchstr
            url='https://www.rcsb.org/search?request='+urlencode(searchdict)
            print (url)
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self,response):
        with open('pdbbank_p1.html','wb') as f:
            f.write(response.body)
        self.log(f'Saved file pdbbank_p1.html')
        
        """
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
        """
