import requests
from bs4 import BeautifulSoup
import os
import re
import errno
import time
import random

# start_html = requests.get(pics_url, headers=headers)
# Soup = BeautifulSoup(start_html.text, 'lxml')
# pic_url = Soup.find('div',class_='main-image').find('p').find('a')
# pic_referer = Soup.find('div',class_='main-image').find('p')

headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url,  headers=headers)


def start():
    Soup = BeautifulSoup(start_html.text, 'lxml')
    all_a = Soup.find('div', class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        href = a['href']
        mkdir(href)

def mkdir(init_url):
    global referer
    global pic_url

    headers={ 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36','referer':all_url }

    start_html = requests.get(init_url, headers = headers)
    Soup = BeautifulSoup(start_html.text, 'lxml')
    folder_name = re.search(r'(\d{2,6})',(Soup.find('div',class_='main-image').find('p').find('a'))['href']).group();

    referer = init_url;

    # get num of pics
    pics = Soup.find('body').find('div', class_='main').find('div',class_='content').find('div',class_='pagenavi').find_all('a')
    #tmp = len(pics)
    tmp = str(pics[len(pics)-2])
    pics_num = int(BeautifulSoup(tmp,'lxml').find('span').string)

    print pics_num

    try:
        os.makedirs(folder_name)
        for x in range(0,pics_num):
            get_pic(folder_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('ok')
        else:
            print('the folder has existed.')
            time.sleep(random.randint(10,30))
            #pass


def get_pic(folder_name):

    global referer
    global pic_url

    print(referer)

    headers={ 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36','referer':referer }
    img_html = requests.get(referer, headers = headers)
    img_Soup = BeautifulSoup(img_html.text, 'lxml')
    pic_url = (img_Soup.find('div',class_='main-image').find('p').img)['src']

    print(pic_url)
    print(referer)

    # save pic.
    name = pic_url[-9:-4]
    print name
    img = requests.get(pic_url, headers=headers)
    f = open(folder_name +'/'+ name + '.jpg', 'ab')
    f.write(img.content)
    f.close()
    print 'pic saved.'
    referer = (img_Soup.find('div',class_='main-image').find('p').find('a'))['href']

    time.sleep(random.randint(10,30))

    return

start()
