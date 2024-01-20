import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
import numpy as np
import csv
from time import sleep

def get_proxies():
    url = 'https://free-proxy-list.net/anonymous-proxy.html'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:30]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def scrape_bloomberg(subject, page_number, headers, proxies):
    full_url = 'https://www.bloomberg.com/search?query=' + subject + '&sort=time:desc' + '&page=' + str(page_number)
    response = requests.get(full_url, headers=headers, proxies = proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    titles = [s.text for s in soup.findAll('a', class_="headline__3a97424275", href = True)]
    ##links = [''.join(s.attrs['href']) for s in soup.findAll('a', class_="headline__3a97424275", href = True)]
    return titles

def getBloombergHeadlines(topic):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.google.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
    }

    subject = topic
    pages_min = 1
    pages_max = 5

    completed_page = pages_min-1
    full = np.array([])

    while completed_page < pages_max:
        proxy_list = get_proxies()
        print(proxy_list)
        for proxy in proxy_list:
            pages = np.arange(completed_page + 1,pages_max+1,1)

            proxies = {
                'http': proxy,
                'https': proxy,
            }

            for page in pages:

                print('Trying Page ' + str(page) + ' using proxy ' + proxy)
                try:
                    full = np.append(full, scrape_bloomberg(subject = subject, page_number = page, headers = headers, proxies = proxies))
                    print('Page ' + str(page) + ' completed\n')
                    completed_page = page
                except Exception as e:
                    print(str(e))
                    print('Failed Page ' + str(page) + ' using proxy ' + proxy)
                    break

    np.savetxt('BloomBerg'+ subject + str(pages_max)+'.csv', full, fmt='%s', delimiter=',')

def scrapeYahooNews(search):
    """Run the main program"""
    template = 'https://news.search.yahoo.com/search?p={}'
    url = template.format(search)
    articles = []
    links = set()
    proxy_list = get_proxies()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.google.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
    }

    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'NewsArticle')
        
        # extract articles from page
        for card in cards:
            article = card.find('h4', 's-title').text
            link = article[-1]
            if not link in links:
                links.add(link)
                articles.append(article)        
        break
            
    # save article data
    with open('YahooNews' + search + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for article in articles:
            writer.writerow([article])
        
    return articles

def scrapeYahooFinanceNews(search):
    """Run the main program"""
    template = 'https://finance.yahoo.com/quote/{}'
    url = template.format(search)
    articles = []
    links = set()

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.google.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
    }
    
    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('.js-stream-content .js-content-viewer')
        
        # extract articles from page
        for card in cards:
            article = card.text
            link = article[-1]
            if not link in links:
                links.add(link)
                articles.append(article)        
        break
            
    # save article data
    with open('YahooFinance' + search + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for article in articles:
            writer.writerow([article])
        
    return articles