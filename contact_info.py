from bs4 import BeautifulSoup
import urllib as urllib
import requests
import re
from googlesearch import search
from lxml import html

def check_website(url):
    resp=requests.get(url)
    soup=BeautifulSoup(resp.text,"lxml")
    
    emails = []
    soupString = str(soup)
    if soupString.find("@")!=-1:
        match = re.search(r'([\w\.-]+)@([\w\.-]+)', soupString)
        if match:
            emails.append(match.group())
        if emails:
            print("email present :",*emails)
    
   # url = ["/contact","/contact.aspx","/main-contact","/#contactus","/contacts.html","/connect-with-us","/contact-us","connect","/contact.html",""]
    url1=""
    for link in soup.findAll('a'):
        l = str(link.string)
        if(l.find("ontact")!=-1 or (l.find("onnect"))!=-1 or str(link).find("onnect")!=-1 or str(link).find("ontact")!=-1):
            match = re.search(r'href=\"([^\s]*)\"',str(link))
            if match:
                redirect = match.group(1)
                if redirect[0]=="/":
                    print(redirect)
                    mat = re.search(r'[\w]*\://[^/]*', url)
                    if mat:
                        url1 = mat.group()
                    else:
                        url1 = url
                    redirect = url1 + redirect
                    print(redirect)
                elif redirect[0]=='#':
                    continue
                
    

#open_website('http://www.filmtack.com/contact/main-contact/')
#check_website('http://www.comfortdelgro.com.sg/web/guest')
check_website('http://www.antlabs.com/')
#check_website('https://www.2c2p.com/index.html')
#check_website('https://www.certissecurity.com/')
#check_website('https://www.aetos.com.sg')
#check_website('http://www.fraserandneave.com/')

#check_website('http://www.filmtack.com/')