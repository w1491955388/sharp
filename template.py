from Spidersystem.main import Master,Slave,Engine
from Spidersystem.request import Request
from Spidersystem.spider import BaseSpider

# 项目名字
PROJECT_NAME = 'test'

# 请求管理配置
REQUEST_MANAGER_CONFIG = {
    'queue_type':'fifo', # 请求队列的类型
    'queue_kwargs':{'host':'127.0.0.1','port':'6379'}, # 请求队列配置
    'filter_type':'redis', # 过滤队列的类型
    'filter_kwargs':{'redis_key':'test','redis_host':'127.0.0.1'} # 过滤队列的配置
}

# 爬虫
class BaiduSpider(BaseSpider):
    name = 'baidu'

    def start_requests(self):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Cookie': 'PSTM=1576555259; BAIDUID=1DFEF2BDFB0386C4AE59070135DBE4CD:FG=1; delPer=0; BD_CK_SAM=1; PSINO=2; BD_UPN=123253; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BIDUPSID=F4AD87BBEFEBDBEAAD6C413280F9944A; H_PS_PSSID=1454_21115_30211_22158; COOKIE_SESSION=11_0_4_5_5_0_0_0_4_0_0_0_6234_0_0_0_1576491897_0_1576555271%7C5%230_0_1576555271%7C1; H_PS_645EC=e385t8SeKpA%2BBIhr%2FecbLOXsoRcWJlnl9IzbzUaq7qOO2%2FOB1yZqA9uh3xA'
        }

        yield Request('http://www.baidu.com/',headers=headers,name=self.name)
        yield Request('https://www.baidu.com/s?wd=tornado4',headers=headers,name=self.name)
        yield Request('https://www.baidu.com/s?wd=tornado8',headers=headers,name=self.name)

    def parse(self,response):

        print(response)
        print(response.url)
        print(response.body)

        yield response.body

    def data_clean(self,data):

        return data

    def data_save(self,data):
        pass

if __name__ == '__main__':
    spiders = {BaiduSpider.name:BaiduSpider}

    master = Master(spiders,project_name=PROJECT_NAME,request_manger_config=REQUEST_MANAGER_CONFIG)
    slave = Slave(spiders,project_name=PROJECT_NAME,request_manger_config=REQUEST_MANAGER_CONFIG)

    Engine().start(master)
    Engine().start(slave)
