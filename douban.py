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

def download_pic(referer,url,headers):
    try:
        headers['Referer'] = referer
        s = requests.Session()
        get_collection_html =  s.get(url,  headers = headers)
        time.sleep(random.randint(1,2))
        return get_collection_html

    except requests.exceptions.ConnectionError as e:
        print(e)
        get_url(referer,url,headers)

    except requests.exceptions.Timeout:
        pass
    # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
        pass
        # Tell the user their URL was bad and try a different one
    except requests.exceptions.RequestException as e:
        pass
        # catastrophic error. bail.
        print e



def get_url(referer,url,headers):
    if referer != '':
        try:
            headers['Referer'] = referer
            s = requests.Session()
            get_collection_html =  s.get(url,  headers = headers)
            time.sleep(random.randint(1,2))
            return BeautifulSoup(get_collection_html.text, 'lxml')

        except requests.exceptions.ConnectionError as e:
            print(e)
            get_url(referer,url,headers)

        except requests.exceptions.Timeout:
            pass
        # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            pass
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            pass
            # catastrophic error. bail.
            print e

    else:
        try:
            s = requests.Session()
            get_collection_html =  s.get(url,  headers = headers)
            time.sleep(random.randint(1,2))
            return BeautifulSoup(get_collection_html.text, 'lxml')

        except requests.exceptions.ConnectionError as e:
            print(e)
            get_url(referer,url,headers)

        except requests.exceptions.Timeout:
            pass
        # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            pass
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            pass
            # catastrophic error. bail.
            print e




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
init_url = 'https://www.douban.com/people/166193223/doulists/collect'


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
    Soup = get_url('', init_url, headers)
    all_collections = Soup.find('div', class_='article').find_all('h3')

    for b in all_collections:
        doulist = b.a['href'] # update the Referer
        get_doulist(init_url, doulist)
        time.sleep(random.randint(1,2))
        break

#doulist_url = get_album_in_each_page( page_ref, doulist, x)
def get_album_in_each_page(page_ref, doulist, x):

    if x == 0:
        page_ref = doulist

    else:
        page_ref = doulist+'?start='+str((x-1)*25)+'&sort=seq&sub_type='
        doulist = doulist +'?start='+str(x*25)+'&sort=seq&sub_type='
        global_doulist = doulist

    Soup = get_url(page_ref, doulist, headers)
    albums_in_this_page = Soup.find_all('div', class_='title')

    return albums_in_this_page


def get_doulist(referer, doulist):

    Soup = get_url(referer, doulist, headers)
    all_doulists = Soup.find_all('div', class_='doulist-item')

    # get num of albums in this doulist
    total_of_albums = Soup.find('a', class_='active').span.get_text()
    total_of_albums = re.findall("\d+",total_of_albums)[0]

    if ( int(total_of_albums) % 25 == 0):
        num_of_pages = int(int(total_of_albums)/25)
    else:
        num_of_pages = int(int(total_of_albums)/25) + 1

    # enter into page of doulists
    for x in range(0,num_of_pages):

        #headers['Referer'] = Referer
        global global_doulist
        global_doulist = doulist
        page_ref = doulist
        album_in_each_page = get_album_in_each_page( page_ref, doulist, x)

        for a in album_in_each_page:
            album_url = a.a['href']
            if re.match('https:\/\/www',str(album_url)):
                get_pics_url(global_doulist, album_url)
                time.sleep(random.randint(1,2))
                sys.exit('ok')

        time.sleep(random.randint(1,2))

        #return


def get_pics_url(global_doulist,album_url):

    Soup = get_url(ref, album_url, headers)
    album = Soup.find('h1').get_text()
    num_of_album = Soup.find('div',class_="pl photitle").span.get_text()
    num_of_album = re.findall("\d+",num_of_album)[0]

    first_pic_url = Soup.find('div',class_='photo_wrap').a['href']

    # print num_of_album


    #sys.exit('ok')

    #global ref
    try:
        os.makedirs(album)
        # for x in range(0,pics_num):
        #     get_pic(folder_name)
        global folder_name
        folder_name = album
        img_ref = album_url
        pic_url = first_pic_url
        y = [img_ref, first_pic_url]
        for x in range(0,int(num_of_album)):

            print y[0]
            print y[1]

            y = get_pic(y[0],y[1],x)
            #time.sleep(random.randint(1,2))

    except OSError as e:
        if e.errno != errno.EEXIST:
            print('ok.')
        else:
            print(album, 'the folder has existed.')
            time.sleep(random.randint(1,2))




def get_pic(pic_ref,pic,x):

    #pic = pic.replace('#image','')
    headers['Host'] = 'www.douban.com'
    Soup = get_url(pic_ref,pic,headers)


    # real image url
    img_url_soup = Soup.find('a',class_="mainphoto").img['src']
    img_url = img_url_soup
    img_url = img_url.replace('webp','jpg')

    #get different host in headers
    host = re.search(r'https://(.*.com)/.*',img_url).group(1)

    # get next pic_url
    next_pic_url = str(Soup.find('a',class_="mainphoto")['href'])
    img_headers = headers
    img_headers['Host'] = host
    name = x
    img = download_pic(pic, img_url, headers)
    f = open(folder_name +'/'+ str(name) + '.jpg', 'ab')
    f.write(img.content)
    f.close()
    pic = pic.replace('#image','')
    res =[pic,next_pic_url]


    print 'pic saved.'

    return res




get_collection()
