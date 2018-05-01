from bs4 import BeautifulSoup
import urllib as urllib
import requests
import re
from googlesearch import search
import json
# from nltk.corpus import stopwords
# from nltk.stem.wordnet import WordNetLemmatizer
# import string
# import gensim
# from gensim import corpora
def primary_info(company_name):
    # user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    # headers={'User-Agent':user_agent,}
    # url="https://www.google.com/search?q="
    # url=url+urllib.parse.quote_plus(company_name+" wiki")
    # #request=
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
                    print(soup.select('span[id="External_links"]')[0].parent.select('+ ul')[0].findChildren()[0].select('a')[0].attrs['href'])
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



# def find_profile(about):
#     docs=about.split(".")
#     stop = set(stopwords.words('english'))
#     exclude = set(string.punctuation)
#     lemma = WordNetLemmatizer()
#     cleaned=[]
#     for localabout in docs:
#         stop_free = " ".join([i for i in localabout.lower().split() if i not in stop])
#         punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
#         normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
#         cleaned.append(normalized)
#     print(normalized)
#     dictionary=corpora.Dictionary(cleaned)
#     doc_term_matrix=dictionary.doc2bow(docs)
#     Lda = gensim.models.ldamodel.LdaModel# Running and Trainign LDA model on the document term matrix.
#     ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
#     print(ldamodel.print_topics(num_topics=3, num_words=3))


def get_website(company):
    for i in range(0,len(data_array)):
        if(list(data_array[i].keys())[0]==company):
            return(list(data_array[i].values())[0]['Website'])

def find_links(org_url):
    url="https://"+org_url
    try:
        resp=requests.get(url)
    except Exception as e:
        print(e)
        url="http://"+org_url
        resp=requests.get(url)
    tags=['a','li','ul','ol','div','span']
    soup=BeautifulSoup(resp.text)
    #print(tags)
    menutags=[]
    linktags=[]
    for tag in tags:
        menutags=soup.find_all(tag,class_=re.compile('.*menu.*'))
        for i in range(0,len(menutags)):
            linktags+=menutags[i].select("[href]")
    return(linktags)

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

def crawl_sub_pages(links):
    links=set(links)
    for link in links:
        print(link.attrs['href'])

#fetch_and_write()
read_from_datasource()
# company='Far East Orchard'

try:
    links_array=[]
    namesfile=open('sourcedata.txt')
    for company in namesfile:
        try:
            org_url=get_website(company.strip())
            print(org_url)
            if(org_url!='NA'):
                links=find_links(org_url)
                links_array.append({company_name:links})
        except:
            pass
    linksfile=open("links_file.json","w",encoding="utf-8")
    json.dump(links_array, linksfile,ensure_ascii=False)

        #crawl_sub_pages(links)
except Exception as e:
    print(e)

# org_url=get_website(company)
#if(org_url!='NA'):
#   print(org_url)
#   links=find_links(org_url)
#   crawl_sub_pages(links)
