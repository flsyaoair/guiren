import os
import urllib   
def getPage():
    url = 'http://192.168.203.14:8081/nexus/content/repositories/releases/skyFS-64/skyFS-storage/'
    page = urllib.urlopen(url)
    html = page.readlines();
    y='.xml'
    x=url
    for i in html:
        if    x in i:
            if not y in i:
                i=i[i.find('href="')+6:i.find('">')]
                geturl=getUrl(i)
                modulename=geturl[geturl.find('">')+2:geturl.find('</a>')]
                print modulename

def getUrl(url):
    page = urllib.urlopen(url)
    html = page.readlines();
    y='.pom'
    x=url
    for i in html:
        if x in i:
            if not y in i:
                return i
bulid= getPage()