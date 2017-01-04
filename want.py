import pandas as pd
import h5py
from wanwang import check
import re

class search_domain():
    #可以指定查询日期，否则查询所有日期的域名
    def __init__(self,date = None):
        self.date = date
    #获取查询日期
    def get_dates(self):
        if self.date is None:
            f = h5py.File('domains.h5','r+')
            dates = f.keys()
        else:
            dates = [self.date]
        return dates
    #获取需要检索的域名
    def get_domains(self):
            dates = self.get_dates()
            domains = {}
            for date in dates:
                domain = pd.read_hdf('domains.h5',key=date)
                domain = pd.Series(domain).fillna('nan')
                domain = pd.np.array(domain)
                domains[date] = domain
            return domains
    #下面是用来检索域名的函数
    #全是字母
    def alpha(self,domains):
        apdomains = {}
        for i in domains.keys():
            apdomain = [j for j in domains[i] if j != 'nan' and j.isalpha()]
            if len(apdomain)>0:
                apdomains[i] = apdomain
        return apdomains
    #字母加数字
    def alnum(self,domains):
        aldomains = {}
        for i in domains.keys():
            aldomain = [j for j in domains[i] if j != 'nan' and j.isalnum()]
            if len(aldomain)>0:
                aldomains[i] = aldomain
        return aldomains
    #全数字
    def digit(self,domains):
        digitdomains = {}
        for i in domains.keys():
            digitdomain = [j for j in domains[i] if j != 'nan' and j.isdigit()]
            if len(digitdomain) > 0:
                digitdomains[i] = digitdomain
        return digitdomains
    #一定长度的域名
    def lendomain(self,s,e,domains):
        lndomains = {}
        for i in domains.keys():
            lndomain = [j for j in domains[i] if j != 'nan' and len(j) in range(s,e+1)]
            if len(lndomain)>0:
                lndomains[i] = lndomain
        return lndomains
    #域名前后中存在指定的字符
    def strin(self,string,domains):
        strdomains = {}
        for i in domains.keys():
            strdomain = [j for j in domains[i] if j != 'nan' and j.startswith(string) or j.endswith(string)]
            if len(strdomain)>0:
                strdomains[i] = strdomain
        return strdomains
    #获取字典中的单词
    def get_words(self):
        wordlist = []
        with open('words.txt', 'r') as w:
            words = w.readlines()
            for word in words:
                wordlist.append(word.strip())
        return wordlist

    #查询字符加单词类域名
    def streng(self,string,domains):
        strengs = {}
        words = self.get_words()
        domains = self.strin(string,domains)
        for i in domains.keys():
            streng = [j for j in domains[i] if j != 'nan' and j.replace(string,'',1) in words]
            if len(streng)>0:
                strengs[i] = streng
        return strengs



    #用来自己编写正则表达式规则进行检索
    def regdomain(self,domains):
        pass


    #用来检索域名是否已注册
    def checkdomain(self, domains, suffix='.com'):
        okdomains = {}
        for i in domains.keys():
            okdomain = [j for j in domains[i] if check(j + suffix) == '210']
            if len(okdomain) > 0:
                okdomains[i] = okdomain
        return okdomains


if __name__ == '__main__':
    a = search_domain()
    b = a.get_domains()
    c = a.alpha(b)
    d = a.alnum(b)
    e = a.streng('vr',b)
    f = a.lendomain(4,6,b)
    g = a.digit(b)
    print(len(c['2017-01-04']))




