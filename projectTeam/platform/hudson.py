# -*- coding: UTF-8 -*- 
import urllib
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = [] 
        self.hudsonvalue = ""
    a_text = False
    l_text = False 

   
    def handle_starttag(self,tag,attr):  
        if tag == 'a': 
            for (i,j) in attr:
                if "last" in j:
                    self.a_text = True  
    def handle_endtag(self,tag):  
        if tag == 'a':  
            self.a_text = False
           
    def handle_data(self,data):
        if self.a_text: 
#             print data
            self.links.append(data)
           
def getPage():
    admin ='admin'
    password ='csst10'
    url = 'http://admin:password@192.168.203.10:8081/hudson/job/09003hzxcqGA_storageServer_ver3.0.1_build/'
    url=url.replace('admin', admin)
    url=url.replace('password', password)
    page = urllib.urlopen(url)
    html = page.read()
    hp = MyHTMLParser()   
    hp.feed(html)   
    hp.close()
    link=hp.links
    for i in link:
        
        if 'Last build' in i:
            
            id=i[i.find('(#')+2:i.find(')')]
        elif 'Last successful'  in i:
             
            id2=i[i.find('(#')+2:i.find(')')]
            if id==id2:
                print "successful"
            else:
                print "failed"
    url=url+id+'/'
    page = urllib.urlopen(url)
    html = page.readlines()
    for value in html:
#         print value
        if '<br />' in value:
#             print value
            versionNumber=value[:value.find('<br')]
            versionNumber=versionNumber.strip()
            print versionNumber
        elif 'Revision' in value:
            versionNumber=value[value.find('</b>:')+5:]
            versionNumber=versionNumber.strip()
            print versionNumber  
    
#     print html

    

bulid= getPage()