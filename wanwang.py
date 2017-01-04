import requests
from bs4 import BeautifulSoup

def check(domain):
    url = "http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=%s"%domain

    html = requests.get(url)
    bsj = BeautifulSoup(html.text,"lxml")
    num = bsj.find("original").get_text()[:3]
    if num == '210':
        print("%s可以注册"%domain)
    elif num == "213":
        print("查询超时，请重新查询")
    elif num == "211":
        print("%s域名已注册"%domain)
    else:
        print("出现未知问题，域名可能即将删除")
    return num
