import requests
import re,time,bson
from lxml import etree
import bson


class Arwu2021():

    def __init__(self):
        # self.mysql_handle = mysql_handle.MysqlHandler(200)
        pass
    def visit_index(self):
        # 访问英文版arwu官网
        url = 'https://www.shanghairanking.cn/api/pub/v1/gras/rank?year=2024&subj_code=RS0103'
        result = requests.get(url,verify=False)
        major_cname = []
        urls = []
        codes = []
        subjCategory = [i.get("subjs") for i in result.json().get("data").get("subjCategory")]
        for i in subjCategory:
            for j in i:
                major_cname.append(j.get("nameCn"))
                urls.append("https://www.shanghairanking.cn/api/pub/v1/gras/rank?year=2024&subj_code={}".format(j.get("code")))
                codes.append(j.get("code"))

        # 入库数据
        for cname,code in zip(major_cname,codes):
            id = bson.objectid.ObjectId().__str__()
            major_ename = ''
            major_cname = cname
            major_url = "http://www.shanghairanking.com/rankings/gras/2024/{}".format(code)
            year_time = 2024
            sql = 'insert into school(id,major_ename,major_cname,year_time,major_url) VALUES (%s,%s,%s,%s,%s)'
            val = (id,major_ename,major_cname,year_time,major_url)
            print(val)


        return urls

    def visit_major(self):
        # country_dict = get_countyr_id()
        urls = self.visit_index()
        # 循环遍历url列表，获取目标字段
        for url in urls:
            r = requests.get(url,verify=False)
            jsonData = r.json().get("data").get("rankings")
            subjs = r.json().get("data").get("subjCategory")
            for i in jsonData:
                data = {}
                data['id'] = bson.objectid.ObjectId().__str__()
                data['year_time'] = "2024"
                data['ranking_text'] = i.get("ranking")
                data['ranking'] = i.get("ranking").split('-')[0]
                for sub in subjs:
                    for j in sub.get("subjs"):
                        if r.url.split('=')[-1] == j.get("code"):
                            data['arwu_id'] = j.get("nameCn")
                            break
                data['update_date_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                data['school_cname'] = i.get("univNameCn")
                data['school_ename'] = " ".join([word.capitalize() for word in i.get("univUpEn").split("-")])
                data['country_region'] = i.get("region")
                data['pub'] = i.get("indData").get("31")
                data['cnci'] = i.get("indData").get("32")
                data['ic'] = i.get("indData").get("33")
                data['top'] = i.get("indData").get("34")
                data['award'] = i.get("indData").get("35")
                data['total_score'] = i.get("score")


                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                # 更新数据库表状态
                sql = "insert INTO %s ( %s ) VALUES ( %s )" % ("school", columns, placeholders)
                values = ['' if str(i)=="None" else str(i) for i in list(data.values())]

                print(values)

                self.mysql_handle.insertOne(sql,values)
                self.mysql_handle.end()





if __name__ == '__main__':
    a = Arwu2021()
    a.visit_index()
    a.visit_major()
