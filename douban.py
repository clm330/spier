import requests
from bs4 import BeautifulSoup
import os
import re
import errno
import time
import random
import sys

# add attr: ['xx'] = yy  , del attr : pop()
# Global
ref = ''
Host = 'www.douban.com'
Connection = 'keep-alive'
UpgradeInsecureRequests = '1'
UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
AcceptEncoding = 'gzip, deflate, br'
AcceptLanguage = 'zh-CN,zh;q=0.8,en;q=0.6'
Cookie = 'bid=iuoVvUtiu3g; ll="118282"; __utma=30149280.1535457660.1487827742.1488519207.1489060532.20; __utmz=30149280.1489060532.20.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ps=y; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1504229770%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; push_noty_num=0; push_doumail_num=0; ap=1; _pk_id.100001.8cb4=53cb68cd52bb435c.1487827741.22.1504232851.1504149596.; _pk_ses.100001.8cb4=*'
Referer = 'https://www.douban.com/people/166193223/doulists/collect'

headers = {'Host':Host,
            'Connection':Connection,
            'Upgrade-Insecure-Requests':UpgradeInsecureRequests,
            'User-Agent':UserAgent,
            'Accept':Accept,
            'Accept-Encoding':AcceptEncoding,
            'Accept-Language':AcceptLanguage,
            'Referer' : Referer
}
#cookies = {'Cookie':Cookie}


def get_collection():
    init_url = 'https://www.douban.com/people/166193223/doulists/collect'
    s = requests.Session()
    get_collection_html =  s.get(init_url,  headers=headers)
    Soup = BeautifulSoup(get_collection_html.text, 'lxml')
    all_collections = Soup.find('div', class_='article').find_all('h3')

    for b in all_collections:
        Referer = b.a['href'] # update the Referer
        doulists = Referer
        get_doulists(doulists)
        time.sleep(random.randint(1,2))
        break


def page_doulist(Referer,x):
    if x == 1:
        pass
    else:
        page_url = Referer +'?start='+str(x*25)+'&sort=seq&sub_type='

    page_url = Referer
    s = requests.Session()
    get_doulist_html =  s.get(page_url,  headers=headers)
    Soup = BeautifulSoup(get_doulist_html.text, 'lxml')
    doulists_of_page = Soup.find_all('div', class_='title')
    return doulists_of_page


def get_doulists(doulists):
    doulist = doulists
    s = requests.Session()
    get_doulist_html =  s.get(doulist,  headers=headers)
    Soup = BeautifulSoup(get_doulist_html.text, 'lxml')
    all_doulists = Soup.find_all('div', class_='doulist-item')
    #num_of_pages = Soup.find_all('div', class_='paginator')

    # get num of doulists
    total_of_doulists = Soup.find('a', class_='active').span.get_text()
    total_of_doulists = re.findall("\d+",total_of_doulists)[0]

    if ( int(total_of_doulists) % 25 == 0):
        num_of_pages = int(int(total_of_doulists)/25)
    else:
        num_of_pages = int(int(total_of_doulists)/25) + 1


    for x in range(0,num_of_pages):

        headers['Referer'] = Referer
        doulist_url = page_doulist(Referer,x)

        for a in doulist_url:
            b = a.a['href']
            if re.match('https:\/\/www',str(b)):
                get_pics_url(b)
                time.sleep(random.randint(1,2))
                sys.exit('ok')

        time.sleep(random.randint(1,2))

        return


def get_pics_url(Referer):
    headers['Referer'] = Referer
    get_pics_url_url = Referer
    s = requests.Session()
    get_pics_url_html =  s.get(get_pics_url_url,  headers = headers)
    Soup = BeautifulSoup(get_pics_url_html.text, 'lxml')
    album = Soup.find('h1').get_text()
    num_of_album = Soup.find('div',class_="pl photitle").span.get_text()
    num_of_album = re.findall("\d+",num_of_album)[0]

    first_pic_url = Soup.find('div',class_='photo_wrap').a['href']


    global ref
    try:
        os.makedirs(album)
        # for x in range(0,pics_num):
        #     get_pic(folder_name)
        for x in range(0,int(num_of_album)):
            ref = first_pic_url
            get_pic(ref)
            time.sleep(random.randint(1,5))



    except OSError as e:
        if e.errno != errno.EEXIST:
            print('ok')
        else:
            print(album, 'the folder has existed.')
            time.sleep(random.randint(1,5))




def get_pic(ref):
    #global ref
    print ref
    headers['Referer'] = ref
    pic_url = ref
    s = requests.Session()
    get_pic__html =  s.get(pic_url,  headers = headers)
    Soup = BeautifulSoup(get_pic__html.text, 'lxml')


get_collection()
