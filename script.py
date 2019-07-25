#GBSTAMPSONLINE
from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen
import re
'''
from fake_useragent import UserAgent
import sqlite3
from fake_useragent import UserAgent
import shutil
from stem import Signal
from stem.control import Controller
import socket
import socks
import requests
import os

controller = Controller.from_port(port=9051)
controller.authenticate()

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor():
    controller.signal(Signal.NEWNYM)

def showmyip():
    url = "http://www.showmyip.gr/"
    r = requests.Session()
    page = r.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    try:
    	ip_address = soup.find("span",{"class":"ip_address"}).text()
    	print(ip_address)
    except:
        print('IP problem')
    
UA = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')

hdr = {'User-Agent': "'"+UA.random+"'",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
'''

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except:
        pass

    return html_content

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('[cellpadding="5"] a img'):
            if item.parent:
                 item_url = 'https://www.gbstampsonline.co.uk/' + item.parent.get('href')   
                 items.append(item_url)
    except: 
        pass

    try:
        next_item = html.find("link", {"rel":"next"})
        next_url = 'https://www.gbstampsonline.co.uk/' + next_item.get('href')   
    except:
        pass

    shuffle(items)

    return items, next_url

def get_categories(url):
    
    items = []
    
    try:
        html = get_html(url)
        for item in html.select('b font a'):
            item_url = 'https://www.gbstampsonline.co.uk/' + item.get('href')
            items.append(item_url)
    except:
        pass
    
    return items

def get_main_categories(url):
    
    items = {}
    
    try:
        html = get_html(url)
        for item in html.select('b font a'):
            item_url = 'https://www.gbstampsonline.co.uk/' + item.get('href')  
            item_name = item.get_text().strip()
            items[item_name] = item_url
    except:
        pass
    
    return items

def get_details(url):

    stamp = {}
    category = ''

    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('#_EKM_PRODUCTPRICE')[0].get_text()
        price = price.replace(",", "").strip()
        stamp['price'] = price
    except:
        stamp['price'] = None
        
    try:
        title = html.find("span", {"itemprop":"name"}).get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
        
    try:
        condition = html.select(".desc strong")[0].get_text().strip()
        stamp['condition'] = condition
    except:
        stamp['condition'] = None    
        
    try:
        category_items = html.select("#blue span a span")
        stamp['category'] = category_items[-2].get_text().strip()
    except: 
        stamp['category'] = None   
        pass   

    try:
        raw_text_temp = html.select('span.desc')[0].get_text().strip()
        raw_text_parts = raw_text_temp.split("\n\n")
        stamp['raw_text'] = raw_text_parts[0].replace("\r\n", " ").replace("\n", " ")
    except:
        stamp['raw_text'] = None
        
    try:
    	temp = stamp['title'].split(' ')
    	stamp['SG']=temp[0]
    	stamp['face_value'] = temp[1]
    except:
    	stamp['SG']=None
    	stamp['face_value'] = None
    stamp['currency'] = 'GBP'
    
    # image_urls should be a list
    images = []
    try:
        image_items = html.find_all("a", {"id" : re.compile('_EKM_PRODUCTIMAGE_LINK_*')})
        for image_item in image_items:
            img_href = image_item.get('href')
            if img_href != '#':
                img = 'https://www.gbstampsonline.co.uk' + img_href
                if img not in images:
                    images.append(img)
    except:
        pass

    stamp['image_urls'] = images

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
    return stamp

def get_details_from_pages(page_url):
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        # loop through all items on current page
        for page_item in page_items:
            stamp = get_details(page_item)
'''
def file_names(stamp):
    file_name = []
    rand_string = "RAND_ze"+str(randint(0,1000000))
    file_name = [rand_string+"-" + str(i) + ".png" for i in range(len(stamp['image_urls']))]
    return(file_name)

def query_for_previous(stamp):
    # CHECKING IF Stamp IN DB
    os.chdir("/Volumes/Stamps/")
    conn1 = sqlite3.connect('Reference_data.db')
    c = conn1.cursor()
    col_nm = 'url'
    col_nm2 = 'raw_text'
    unique = stamp['url']
    unique2 = stamp['raw_text']
    c.execute('SELECT * FROM zeboose WHERE "{cn}" LIKE "{un}%" AND "{cn2}" LIKE "{un2}%"'.format(cn=col_nm, cn2=col_nm2, un=unique, un2=unique2))
    all_rows = c.fetchall()
    conn1.close()
    price_update=[]
    price_update.append((stamp['url'],
    stamp['raw_text'],
    stamp['scrape_date'], 
    stamp['price'], 
    stamp['currency']))
    
    if len(all_rows) > 0:
        print ("This is in the database already")
        conn1 = sqlite3.connect('Reference_data.db')
        c = conn1.cursor()
        c.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn1.commit()
        conn1.close()
        print (" ")
        #url_count(count)
        sleep(randint(10,45))
        next_stemp = 'continue'
    else:
        os.chdir("/Volumes/Stamps/")
        conn2 = sqlite3.connect('Reference_data.db')
        c2 = conn2.cursor()
        c2.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn2.commit()
        conn2.close()
        next_step = 'pass'
    print("Price Updated")
    return(next_step)

def db_update_image_download(stamp): 
    req = requests.Session()
    directory = "/Volumes/Stamps/stamps/zeboose/" + str(datetime.datetime.today().strftime('%Y-%m-%d')) +"/"
    image_paths = []
    names = file_names(stamp)
    image_paths = [directory + names[i] for i in range(len(names))]
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    for item in range(0,len(names)):
        print (stamp['image_urls'][item])
        try:
            imgRequest1=req.get(stamp['image_urls'][item],headers=hdr, timeout=60, stream=True)
        except:
            print ("waiting...")
            sleep(randint(3000,6000))
            print ("...")
            imgRequest1=req.get(stamp['image_urls'][item], headers=hdr, timeout=60, stream=True)
        if imgRequest1.status_code==200:
            with open(names[item],'wb') as localFile:
                imgRequest1.raw.decode_content = True
                shutil.copyfileobj(imgRequest1.raw, localFile)
                sleep(randint(18,30))
    stamp['image_paths']=", ".join(image_paths)
    #url_count += len(image_paths)
    database_update =[]

    # PUTTING NEW STAMPS IN DB
    database_update.append((
        stamp['url'],
        stamp['raw_text'],
        stamp['title'],
        stamp['scott_num'],
        stamp['SG'],
        stamp['country'],
        stamp['year'],
        stamp['category'],
        stamp['sku'],
        stamp['scrape_date'],
        stamp['image_paths']))
    os.chdir("/Volumes/Stamps/")
    conn = sqlite3.connect('Reference_data.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("""INSERT INTO zeboose ('url','raw_text', 'title', 'scott_num','SG',
    'country','year','category','sku','scrape_date','image_paths') 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", database_update)
    conn.commit()
    conn.close()
    print ("all updated")
    print ("++++++++++++")
    print (" ")
    sleep(randint(45,140))
'''

count = 0
#connectTor()

# choose input category
categories = get_main_categories('https://www.gbstampsonline.co.uk')
for category_item in categories.items():
    print(category_item)

selected_category_name = input('Make a selection: ')
category = categories[selected_category_name]

# loop through all subcategories of input category
subcategories = get_categories(category)
shuffle(subcategories)
if subcategories:
    for subcategory in subcategories:
    	count += 1
    	# loop through all subcategories of level 2
    	subcategories2 = get_categories(subcategory)
    	if subcategories2:
    		page_urls = subcategories2
    	else:
    		page_urls = [subcategory]
    	shuffle(page_urls)
    	for page_url in page_urls:
    		print (page_url)
    		count += 1
    		if count > randint(75, 156):
    			print('Sleeping...')
    			sleep(randint(500, 2000))
    			#connectTor()
    			count = 0
    		else:
    			pass
    		get_details_from_pages(page_url)
    		'''
        	next_step = query_for_previous(stamp)
            if next_step == 'continue':
            	print('Only updating price')
            	continue
            elif next_step == 'pass':
            	print('Inserting the item')
            		pass
            else:
            	break
            db_update_image_download(stamp)
            '''
else:
    get_details_from_pages(category)
    
    