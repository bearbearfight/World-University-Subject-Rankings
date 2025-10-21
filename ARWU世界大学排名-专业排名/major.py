import pymysql
import requests
from lxml import etree
# from mpl_toolkits.axes_grid1 import host_subplot
from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray
import bson
import pymysql

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
# }

url = "https://www.shanghairanking.com/rankings/gras/2024"

#这里配置你的数据库
conn = ()

cursor = conn.cursor()
response = requests.get(url)
response.encoding = 'utf-8'
page_text = response.text
# print(page_text)
tree = etree.HTML(page_text)

div_list = tree.xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div/div[2]/div')
# item = {}
for div in div_list:
    id = bson.objectid.ObjectId().__str__()
    major_ename = div.xpath('./a/span/text()')[0]
    major_cname = ''
    # print(id)
    year_time = 2024
    major_url = "https://www.shanghairanking.com"+div.xpath('./a/@href')[0]
    # print(major_url)
    major_classify_id = ''


