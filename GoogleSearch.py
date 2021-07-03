import pretty_errors #Error Package
from magic_google import MagicGoogle #Google Search Package
import codecs #Write File Package
from datetime import datetime #Datetime Package
from re import search, sub, compile, IGNORECASE #Regular Expression Package
from tqdm import tqdm #Process Bar Package
from os import remove #Removal Package

#Scrape Setting
target_language = 'ha' #Choosing from en/pidgin/ha
scrape_language = 'ha' #Choosing from en/ha
scrape_mode = 'c' #Choosing from u/s
scrape_repeat_time = 999999999999999999 #Amount to Scrape
scrape_pause_time = 50 #Pause for Scraper

'''
Scraper Setting Recommendation
#English Scraper:
#Pidgin Scrpaper:
#Hausa Scraper:
'''

#Path for Seached URLs
save_url_path = '//Users//nitrolichtung//Downloads//Movie//google_search//{}_url_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
#Path for Searched Titles
save_title_path = '//Users//nitrolichtung//Downloads//Movie//google_search//{}_title_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
clean_title_path = '//Users//nitrolichtung//Downloads//Movie//google_search//{}_title_clean_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
#Path for Searched Texts
save_desc_path = '//Users//nitrolichtung//Downloads//Movie//google_search//{}_desc_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
clean_desc_path = '//Users//nitrolichtung//Downloads//Movie//google_search//{}_desc_clean_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
#Path for Searching Keywords
keywords_path = '//Users//nitrolichtung//Desktop//scrape_keywords//{}_keywords_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)

#Proxy Poll Setting, 'proxy_pool = None' for No Proxy Mode
proxy_pool = [{
    'http': 'http://127.0.0.1:7890',
}]

#Read Keyword File into List
search_list = []
with codecs.open(keywords_path, mode='r', encoding='utf-8') as keywords:
    for keyword in keywords:
        search_list.append(keyword.strip('\n'))

#Define Search Object
magic_google = MagicGoogle(proxies=proxy_pool)

#Define Search Process Bar
process_bar_search = tqdm(total = len(search_list) * 2)

#Search and Save URLs
for search_query in search_list: 
    for url in magic_google.search_url(query=search_query, language=scrape_language, num=scrape_repeat_time ,pause=scrape_pause_time):
        with codecs.open(save_url_path, mode='a', encoding='utf-8') as url_file:
            if url.isspace()==False and len(url.strip('\n'))>0: #Dump Empty URL
                url_file.write(url.strip('\n') + '\n')
            else:
                url_file.write('[EmptyURL]\n')
    process_bar_search.set_description('searched %s url' % search_query)
    process_bar_search.update(1)

#Search and Save Titles
for search_query in search_list: 
    for content in magic_google.search(query=search_query, language=scrape_language, num=scrape_repeat_time ,pause=scrape_pause_time):
        with codecs.open(save_title_path, mode='a', encoding='utf-8') as title_file:
            if content['title'].isspace()==False and len(content['title'].strip('\n'))>0: #Dump Empty Title
                title_file.write(content['title'].strip('\n') + '\n')
            else:
                title_file.write('[EmptyTitle]\n')

#Search and Save Texts
        with codecs.open(save_desc_path, mode='a', encoding='utf-8') as desc_file:
            if content['text'].isspace()==False and len(content['text'].strip('\n'))>0: #Dump Empty Text
                desc_file.write(content['text'].strip('\n') + '\n')
            else:
                desc_file.write('[EmptyText]\n')
    process_bar_search.set_description('searched %s content' % search_query)
    process_bar_search.update(1)

process_bar_search.close() #Search Process Complete

#Clean Files and Process Empty, Website and Timestamp Lines
def clean_text_file(save_path, clean_path, entity):
    clean_lines = []
    url_pattern = compile(
    r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'\
        , IGNORECASE) #Define URL Pattern
    with codecs.open(save_path, mode='r', encoding='utf-8') as save_file:
        for line in save_file:
            line = sub(url_pattern, '[WebsiteAddress]', line)
            if len(line.strip('\n'))>0 and\
                line.strip('\n') not in clean_lines and\
                not bool(search('\d\sdays?\sago', line)) and\
                not bool(search('\d\sweeks?\sago', line)) and\
                not bool(search('\d\smonths?\sago', line)):
                clean_lines.append(line.strip('\n'))
            else:
                continue
    with codecs.open(clean_path, mode='a', encoding='utf-8') as clean_file:
        for clean_line in clean_lines:
            clean_file.write(clean_line + '\n')
    remove(save_path)
    print('cleaning {} is complete, check your path:\n{}'.format(entity, clean_path))

#Clean URL, Title and Desc File
clean_text_file(save_title_path, clean_title_path, 'title')
clean_text_file(save_desc_path, clean_desc_path, 'content')
