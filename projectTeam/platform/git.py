# -*- coding: UTF-8 -*- 
import urllib
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = [] 
#        self.keyValue ='' 
    a_text = False
    i_text = False 

   
    def handle_starttag(self,tag,attr):  
        if tag == 'a':  
            for (variable,value) in attr:
                if value=='list subject':
                    for (variable,value) in attr:
                            if variable=='href': 
                                self.a_text = True
                                self.links.append(value)
                elif value=='list':
                    self.a_text = True    
        elif tag == 'i' :
            self.i_text = True  
               
    def handle_endtag(self,tag):  
        if tag == 'a':  
            self.a_text = False
        elif tag == 'i':
            self.i_text = False 
                  
              
    def handle_data(self,data):
        if self.a_text: 
            self.links.append(data) 
        
        elif self.i_text:
            self.links.append(data)
                  
def getPage(url,task_key):
#     admin ='admin'
#     password ='123456'
#     ip='192.168.203.211/gitweb'
#     reops ='CheckpointDataGateway'
#     branch ='master'
    task_key='添加索引' 
#     url = 'http://admin:password@ip/?p=reops.git;a=shortlog;h=refs/heads/branch'
#     url=url.replace('admin', admin)
#     url=url.replace('password', password)
#     url=url.replace('ip', ip)
#     url=url.replace('reops', reops)
#     url=url.replace('branch', branch)
    page = urllib.urlopen(url)
    html = page.read()
    hp = MyHTMLParser()   
    hp.feed(html)   
    hp.close()
    for i in hp.links:
        if task_key in i: 
#             存入commitversion数据库 返回页面commitversion
                       
                task_key=i
        else:
             print ''
#            读取   commitversion数据库 返回    
    i=hp.links.index(task_key)
    gitcommit= hp.links[2]
    commitversion=gitcommit[gitcommit.find('h=')+2:]
    print gitcommit

    print(hp.links) 

    return commitversion
