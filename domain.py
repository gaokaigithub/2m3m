import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import os
import h5py


class domain():
    def __init__(self,url):
        self.url = url
    #用来获取某一页的域名
    def get_domain(self,url):
        domain_list = []
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        html = requests.get(url,headers = headers).text
        bsj = BeautifulSoup(html, 'lxml')
        trs = bsj.find_all('tr')

        if len(trs) < 2: return None
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) > 0:
                a = tds[0]
                domain_list.append(a.get_text().replace('.com', ''))
        return domain_list

    #获取某一时间所有页的域名
    def all_domains(self,t,url):
        domains = []
        durl = url
        bi = 0
        i =  1
        while i:
            try:
                if self.get_domain(durl):
                    domain_list = self.get_domain(durl)
                    domains.extend(domain_list)
                    durl = url+'&page='+str(i-1)
                    print('正在获取%s第%d页'%(t,i))
                    i = i+1
                    time.sleep(1)
                else:
                    print('该日期已爬取完啦')
                    break
            except:
                bi = bi+1
                print('这一页没有爬取到')
                if bi>5:
                    print('ip可能已经被ban了，赶紧检查一下吧')
                    break
                continue
        return domains

    #获取时间，用于构造url
    def get_time(self,n=4):
        now = datetime.datetime.now()
        nd = []
        if os.path.exists('domains.h5'):
            nd.append((now+datetime.timedelta(days = n)).strftime('%Y-%m-%d'))
        else:
            for i in range(1,n+1):
                ndays = datetime.timedelta(days=i)
                aday = now+ndays
                nd.append(aday.strftime('%Y-%m-%d'))
            nd.append(now.strftime('%Y-%m-%d'))
        return nd
    #获取url
    def get_url(self):
        nd = self.get_time()
        nurls = {}
        for i in nd:
            nurls[i] = self.url.format(i)
        return nurls
    #获取所选时间的所有域名
    def get_all_time_domain(self):
        nurls = self.get_url()
        ta_domains = {}
        for i in nurls.keys():
            domains = self.all_domains(i,nurls[i])
            if len(domains) == 0:
                print('%s域名尚未更新'%i)
                continue
            ta_domains[i] = pd.Series(domains)
        print('域名获取结束')
        df_domains = pd.DataFrame(ta_domains)
        if len(nurls)>1:
            self.save_domains(df_domains)
        else:
            self.update_domains(df_domains)
        return df_domains

    #将域名保存为hdf5格式，以时间作为列名
    def save_domains(self,df):
        hdf = pd.HDFStore('domains.h5')
        for t in df.columns:
            hdf[t] = df[t]
        hdf.close()
    #更新域名列表并保存
    def update_domains(self,df):
        bday = (datetime.datetime.now() - datetime.timedelta(days = 4)).strftime('%Y-%m-%d')
        f = h5py.File('domains.h5', 'r+')
        if bday in f.keys():
            f.pop(bday)
            f.close()
            self.save_domains(df)
        else:
            f.close()
    #检查是否已更新，更新了再去爬取，可以定时检测一下
    def is_update(self):
        if not os.path.exists('domains.h5'):
            print('第一次爬取，时间要久一些，喝杯咖啡吧')
            return True
        nurls = self.get_url()
        for url in nurls.values():
            if self.get_domain(url):
                print('域名已更新，可以去爬啦')
                return True
            else:
                print('域名尚未更新，歇一会')
                return None

if __name__ == '__main__':
    url = 'http://www.2m3m.com/s/?key=&gc=radom&nokey1=&nokey2=&nokey3=&min=0&max=0&com=com&f=3&f=on&b=on&d={0}&dt=0&o=o_4&pp=100'
    a = domain(url)
    if a.is_update():
        a.get_all_time_domain()