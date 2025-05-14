from sklearn.feature_extraction.text import TfidfVectorizer
from deep_translator import GoogleTranslator
from datetime import datetime
import pypeln.thread as th
import requests
from urllib.parse import urlparse
from dateutil import parser
from bs4 import BeautifulSoup

def _convert_to_date(date):
    try:
        date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        format_date = date_obj.strftime("%Y-%m-%d")
        reconvert = datetime.strptime(format_date,"%Y-%m-%d")
        return reconvert
    except ValueError:
        date_obj = parser.parse(date)
        format_date = date_obj.strftime("%Y-%m-%d")
        reconvert = datetime.strptime(format_date,"%Y-%m-%d")
        return reconvert
    
def _handle_request(link):
    headers = headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    res = requests.get(link, headers=headers)
    return res.content

def _handle_parsing(content, parser = 'xml', link=''):
    soup = BeautifulSoup(content, parser)
    if (urlparse(link).netloc == 'www.washingtonpost.com') & (parser == "html.parser"):
        try:
            p_tag = soup.find(class_='grid-layout').find_all('p')
            paragraphs = list(map(lambda x: x.text, p_tag))
            text = ' '.join(paragraphs)
            return text
        except AttributeError:
            pass
    elif (urlparse(link).netloc == 'www.foxnews.com') & (parser == "html.parser"):
        parsed = ' '.join(list(map(lambda x: x.text ,soup.find_all('p')[2:-5])))
        return parsed
    
    elif (urlparse(link).netloc == 'www.cnbc.com') & (parser == "html.parser"):
        parsed = ' '.join(list(map(lambda x: x.text ,soup.find_all('p')[-21:-6])))
        return parsed
    
    elif (urlparse(link).netloc == 'news.detik.com') & (parser == "html.parser"):
        parsed = soup.find('div', class_='detail__body-text itp_bodycontent')
        if parsed:
            return parsed.text
        else:
            return ''
    
    else:
        parsed = soup.find_all('item') if parser == 'xml' else ' '.join(list(map(lambda x: x.text ,soup.find_all('p'))))
        return parsed

def _get_content(link):
    content = _handle_request(link)
    content_parsed = _handle_parsing(content, parser = 'html.parser',link=link)
    return content_parsed

def _get_attribute(link, n_news, start_date, end_date):
    content = _handle_request(link)
    content_parsed = _handle_parsing(content)
    list_title = []
    list_link = []
    list_pubDate = []
    list_content = []

    def process_item(item):
        pubDate_text = item.find('pubDate').text
        pubDate = _convert_to_date(pubDate_text)

        if (start_date == None) and (end_date == None):
            title = item.find('title').text
            link = item.find('link').text
            pubDate = item.find('pubDate').text
            content = _get_content(link)
            return title, link, pubDate, content
        
        elif (start_date != None) and (end_date != None):
            if (start_date <= pubDate <= end_date):
                title = item.find('title').text
                link = item.find('link').text
                pubDate = item.find('pubDate').text
                content = _get_content(link)
                return title, link, pubDate, content
        
        elif start_date:
            if (pubDate >= start_date):
                title = item.find('title').text
                link = item.find('link').text
                pubDate = item.find('pubDate').text
                content = _get_content(link)
                return title, link, pubDate, content
        elif end_date:
            if (pubDate <= end_date):
                title = item.find('title').text
                link = item.find('link').text
                pubDate = item.find('pubDate').text
                content = _get_content(link)
                return title, link, pubDate, content

    
    results = th.map(process_item, content_parsed[:n_news], workers=5)
    
    for result in results:
        if result is not None:
            title, link, pubDate, content = result
            list_title.append(title)
            list_link.append(link)
            list_pubDate.append(pubDate)
            list_content.append(content)

    # if (start_date == None) and (end_date == None):
    #     for i in range(n_news):
    #         list_title.append(content_parsed[i].find('title').text)
    #         list_link.append(content_parsed[i].find('link').text)
    #         list_pubDate.append(content_parsed[i].find('pubDate').text)
    #         list_content.append(
    #                 _get_content(
    #                     content_parsed[i].find('link').text
    #                 )
    #             )
    
    # elif (start_date != None) and (end_date != None):
    #     for i in range(n_news):
    #         pubDate = _convert_to_date(content_parsed[i].find('pubDate').text)
    #         if (pubDate >= start_date) & (pubDate <= end_date):
    #             list_title.append(content_parsed[i].find('title').text)
    #             list_link.append(content_parsed[i].find('link').text)
    #             list_pubDate.append(content_parsed[i].find('pubDate').text)
    #             list_content.append(
    #                 _get_content(
    #                     content_parsed[i].find('link').text
    #                 )
    #             )
    
    # elif start_date:
    #     for i in range(n_news):
    #         pubDate = _convert_to_date(content_parsed[i].find('pubDate').text)
    #         if pubDate >= start_date:
    #             list_title.append(content_parsed[i].find('title').text)
    #             list_link.append(content_parsed[i].find('link').text)
    #             list_pubDate.append(content_parsed[i].find('pubDate').text)
    #             list_content.append(
    #                 _get_content(
    #                     content_parsed[i].find('link').text
    #                 )
    #             )
    # elif end_date:
    #     for i in range(n_news):
    #         pubDate = _convert_to_date(content_parsed[i].find('pubDate').text)
    #         if pubDate <= end_date:
    #             list_title.append(content_parsed[i].find('title').text)
    #             list_link.append(content_parsed[i].find('link').text)
    #             list_pubDate.append(content_parsed[i].find('pubDate').text)

    #             list_content.append(
    #                 _get_content(
    #                     content_parsed[i].find('link').text
    #                 )
    #             )
        
        

    return list_title, list_link, list_pubDate, list_content

def _translate(text, tl):
    translator = GoogleTranslator(source='auto', target=tl)
    translated_text = translator.translate(text)
    return translated_text
