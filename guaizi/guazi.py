from  lxml import  etree
import requests
import time
import pandas as pd

from jobbole.tools.Script import get_cookie


def crawl(page_num):
    time.sleep(2)
    for i in range(1,page_num+1):
        print('爬取第{}页'.format(i))
        url = 'https://www.guazi.com/www/buy/o{}/#bread'.format(i)
        deal_page(url)

def  deal_page(url):

        response = requests.get(url, headers=head,timeout=(2,2))
        html = etree.HTML(response.text)
        hrefs = html.xpath('//ul[@class="carlist clearfix js-top"]/li/a/@href')
        for href in hrefs:
            car_url = 'https://www.guazi.com'+href
            deal_info(car_url)

def  deal_info(url):
    response = requests.get(url, headers=head, timeout=(2, 2))
    html = etree.HTML(response.text)
    title = html.xpath("//h2[@class='titlebox']/text()")[0].strip()         #售车标题
    license_time=html.xpath("//*[@class='one']/span/text()")[0]     #上牌时间
    Kilometre_number=html.xpath("//*[@class='two']/span/text()")[0] #公里数
    city =html.xpath("//*[@class='three']/span/text()")[0]          #上牌地
    displacement =html.xpath("//*[@class='three']/span/text()")[1]   #排量
    gear_box = html.xpath("//*[@class='last']/span/text()")[0]      #变速箱
    price = float(html.xpath("//*[@class='pricestype']/text()")[0].replace('¥',''))*10000
    base_param1 = html.xpath("//*[@class='td1']/text()")
    base_param2 =html.xpath("//*[@class='td2']/text()")
    from matplotlib.cbook import flatten
    base_param = list(flatten(zip(base_param1,base_param2)))
    param = ','.join(base_param)
    try:
        dataframe = pd.DataFrame({'售车标题': title, '上牌时间': license_time,'公里数':Kilometre_number,'上牌地':city,
                                  '排量':displacement,'变速箱':gear_box,'价格':price,'汽车参数':[param]})
        dataframe.to_csv("car.csv", index=False, sep=',',mode='a')
    except Exception as e:
        print(e)



page_num = 2000
url = 'https://www.guazi.com/www/buy/o1/#bread'


cookie=get_cookie(url)
head ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
       'Cookie':cookie}
crawl(page_num)




