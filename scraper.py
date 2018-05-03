from bs4 import BeautifulSoup
import urllib as urllib
import requests
import re
from googlesearch import search
import json

def primary_info(company_name):
    print(company_name)
    info_dict={}
    wiki_url=""
    for url in search(company_name+" company wiki", stop=1):
            wiki_url=url
            break
    resp=requests.get(wiki_url)
    soup=BeautifulSoup(resp.text)
    #fetching about from wikipedia intro about the company
    try:
        info_dict['About']=soup.select('div.mw-parser-output > p')[0].text
    except:
        info_dict['About']='NA'
    info_tables=soup.find_all('table',class_='infobox')
    # print(info_tables[0].parent.select('p')[0].text)
    #if info table is available, scraping it to get the data and makeing it a dict
    foundWebsite=False
    if(len(info_tables)>0):
        table=info_tables[0]
        rows=table.findAll('tr')
        heads=table.findAll('th')
        data=table.select(' th + td')

        for i in range(0,len(heads)):
            try:

                if(heads[i].text.strip()=='Website'):
                    foundWebsite=True
                    info_dict[heads[i].text.strip()]=data[i].select("a")[0].attrs['href']
                else:
                    info_dict[heads[i].text.strip()]=data[i].text.strip()
            except:
                pass
            #print(heads[i].text,data[i].text)
    #if table isnt available, searching the external links to find the company official website
    if(not foundWebsite):
        try:
            if(len(soup.select('span[id="External_links"]'))>0):
                website=soup.select('span[id="External_links"]')[0].parent.select('+ ul')[0].findChildren()[0].select('a')[0].attrs['href']
                if(website!=None and len(website)>0):
                    info_dict['Website']=website
                    #print(soup.select('span[id="External_links"]')[0].parent.select('+ ul')[0].findChildren()[0].select('a')[0].attrs['href'])
                else:
                    info_dict['Website']='NA'
            else:
                info_dict['Website']='NA'
        except:
            info_dict['Website']='NA'

            #print(extenral)
            #print(rows[i].text)

    # response = requests.get(url,headers=headers)
    # print(response.text)
    # soup=BeautifulSoup(response.text)
    # items=soup.find_all("h3",{'class':'r'})[0]
    # #items=soup.find_all("h3", {"original_target" :re.compile(r".*")})
    # print(items)
    return info_dict





def get_website(company):
    for i in range(0,len(data_array)):
        if(list(data_array[i].keys())[0]==company):
            return(list(data_array[i].values())[0]['Website'])

def find_links(org_url):
    if(not org_url.startswith("http")):
        url="https://"+org_url
        #print("line 109")
        print(url)
        try:
            resp=requests.get(url)
        except Exception as e:
            print(e)
            url="http://"+org_url
            resp=requests.get(url)
    else:
        resp=requests.get(org_url)
    tags=['a','li','nav','ul','ol','div','span','footer']
    soup=BeautifulSoup(resp.text)
    #print(tags)
    menutags=[]
    linktags=[]
    for tag in tags:
        menutags=soup.find_all(tag)
        for i in range(0,len(menutags)):
            linktags+=menutags[i].select("[href]")
            #print(linktags)
    # navtags=soup.find_all('nav')
    # for i in range(0,len(navtags)):
    #     linktags+=navtags[i].select("[href]")
    # if(len(linktags)==0):
    #     print("finding addtional links")
    #     localtags=soup.find_all('a')
    #     for i in range(0,len(localtags)):
    #         linktags+=navtags[i].select("[href]")
    print(org_url)
    #print(len(linktags))
    return(linktags)

def find_and_write_links():
    try:
        links_array=[]
        namesfile=open('sourcedata.txt')
        for company in namesfile:
            try:
                org_url=get_website(company.strip())
                print(org_url)
                if(org_url!='NA'):
                    links=find_links(org_url)
                    comp_link_array=get_navigatable_links(links)
                    print(comp_link_array)
                    #print(comp_link_array)
                    links_array.append({company.strip():comp_link_array})
                    #print(links_array)
            except:
                pass
        linksfile=open("links_file.json","w",encoding="utf-8")
        json.dump(links_array, linksfile,ensure_ascii=False)

            #crawl_sub_pages(links)
    except Exception as e:
        print(e)

def fetch_and_write():
    file=open('sourcedata.txt')
    outputfile=open('database.json', 'w',encoding='utf-8')
    outputlist=[]
    for line in file:
        if(len(line)<=0):
            pass
        else:
            data={line.strip():primary_info(line)}
            outputlist.append(data)
    json.dump(outputlist, outputfile,ensure_ascii=False)

def read_from_datasource():
    global data_array
    data_file=open('database.json',encoding='utf-8')
    data_array=json.load(data_file)


def get_navigatable_links(links):
    links=set(links)
    hrefs=[]
    for link in links:
        hrefs.append(link.attrs['href'].lower())
    return list(set(hrefs))

def categorise_links(sub_links):
    #print(sub_links)
    try:
        categorized_links={"about":[],"contact":[],"news":[],"blog":[],"investor":[],"others":[]}
        #print(len(sub_links))
        for sub_link in sub_links:
            #print(sub_link)
            if("about" in str(sub_link) or "profile" in str(sub_link)):
                #print("found about")
                categorized_links['about'].append(sub_link)
            elif("contact" in str(sub_link) or
            "reach" in str(sub_link) or
            "support" in str(sub_link) or
            "enquire" in str(sub_link) or
            "customer-service" in str(sub_link) or
            "support" in str(sub_link) or
            "help" in str(sub_link)):
                categorized_links['contact'].append(sub_link)
            elif("news" in str(sub_link) or "press" in str(sub_link) or "media" in str(sub_link)):
                categorized_links['news'].append(sub_link)
            elif("investor" in str(sub_link) or "partner" in str(sub_link) ):
                categorized_links['investor'].append(sub_link)
            elif("blog" in str(sub_link) or "story" in str(sub_link)):
                categorized_links['blog'].append(sub_link)
            else:
                categorized_links['blog'].append(sub_link)
    except Exception as e:
        print(e)



    return(categorized_links)

def get_full_sub_url(company_name,i):
    url=""
    if(not i.startswith('http')):
        company_url=get_website(company_name)
        if(i.startswith("/") and not company_url.endswith("/")):
            url=company_url+i
        elif(i.startswith("/") and company_url.endswith("/")):
            url=company_url+i[1:]
        elif(company_url.endswith("/")):
            url=get_website(company_name)+i
        else:
            url=get_website(company_name)+"/"+i

    else:
        url=i
    print("formed"+url)
    return url

comp_contact_dict={}
def crawl_sub_pages(company_name):
    try:
        links_file=open('links_file.json',encoding='utf-8')
        links_array=json.load(links_file)
        global comp_contact_dict
        comp_contact_dict[company_name]=[]
        for i in links_array:
            if(list(i.keys())[0]==company_name):
                sub_links=list(i.values())[0];
                categorized=categorise_links(sub_links)
                company_url=get_website(company_name)
                #print(categorized)
                #print(company_url)
                print(company_name)
                for i in categorized.keys():
                    print(i+str(len(categorized[i])))
                if(len(categorized['contact'])>0):
                    for i in categorized['contact']:
                        url=get_full_sub_url(company_name,i)
                        resp=requests.get(url)
                        num_set=[]
                        contacts=re.findall('([+\(]+([\s\-\(\{\[]*[\d]+[\)\]\}]*){7,10})',str(resp.text))
                        if(len(contacts)>0):
                            for number in contacts:
                                num_set.append(number[0])
                            #print(num_set)
                            comp_contact_dict[company_name]=comp_contact_dict[company_name] + num_set
                elif(len(categorized['about'])>0):
                    for in_i in categorized['about']:
                        url=get_full_sub_url(company_name,i)
                        resp=requests.get(url)
                        num_set=[]
                        abt_contacts=re.findall('([+\(]+([\s\-\(\{\[]*[\d]+[\)\]\}]*){7,10})',str(resp.text))
                        if(len(abt_contacts)>0):
                            for number in abt_contacts:
                                num_set.append(number[0])
                            comp_contact_dict[company_name]=comp_contact_dict[company_name] + num_set
                else:
                    resp=requests.get(company_url)
                    num_set=[]
                    home_contacts=re.findall('([+\(]+([\s\-\(\{\[]*[\d]+[\)\]\}]*){7,10})',str(resp.text))
                    if(len(home_contacts)>0):
                        for number in home_contacts:
                            num_set.append(number[0])
                        comp_contact_dict[company_name]=comp_contact_dict[company_name] + num_set


                    #print(re.findall('([+\(\d]+([\s\-\(\{\[]*[\d]+[\)\]\}]*){7,10})',"(65) 6786 2866")[1

            else:
                pass
        #print(comp_contact_dict)
            #print("No link found :(  ")
    except Exception as e:
        print(e)


#fetch all wiki info and official website
#fetch_and_write()
#read from the data source and store in a global variable
read_from_datasource()
#find all navigable links
#find_and_write_links()
#crawl_sub_pages('Near')
#crawl_sub_pages('ABR Holdings Ltd')
#crawl_sub_pages('FilmTack')
f=open("sourcedata.txt")
for line in f:
    #print(line)
    print(line)
    crawl_sub_pages(line.strip())
#crawl_sub_pages('Venture Corporation')
# company='Far East Orchard'



# org_url=get_website(company)
#if(org_url!='NA'):
#   print(org_url)
#   links=find_links(org_url)
#   crawl_sub_pages(links)
