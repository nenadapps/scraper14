#GBSTAMPSONLINE
from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen
import re
#from fake_useragent import UserAgent

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
        parts = html.select('span.desc')[0].get_text().split("\r\n")
        for part in parts:
            if 'SG' in part and ' ' not in part:
                stamp['SG'] = part
                break
            if 'Set of' in part:
                stamp['set'] = part
                break
    except:
        stamp['SG'] = None
        stamp['set'] = None

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

# choose input category
categories = get_main_categories('https://www.gbstampsonline.co.uk')
for category_item in categories.items():
    print(category_item)

selected_category_name = input('Make a selection: ')
category = categories[selected_category_name]

# loop through all subcategories of input category
subcategories = get_categories(category)
if subcategories:
    for subcategory in subcategories:
        # loop through all subcategories of level 2
        subcategories2 = get_categories(subcategory)
        if subcategories2:
            page_urls = subcategories2
        else:
            page_urls = [subcategory]
        for page_url in page_urls:       
            get_details_from_pages(page_url)
else:
    get_details_from_pages(category)
    
    