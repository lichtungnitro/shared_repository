#import pretty_errors #Error Package
import codecs #Write File Package
from pytrends.request import TrendReq #Google Trends Package
from google_trans_new import google_translator #Google Translation Package
from datetime import datetime #Datetime Package
from os import remove #Removal Package

#Scrape Global Setting
scrape_pause_time = 1 #Pause for Scraper

#Path for Searching Keywords
keywords_path = '//Users//nitrolichtung//Desktop//scrape_keywords//keywords.txt'

#Generate Keywords Path
def generate_keywords_path(scrape_language, scrape_mode):
    keywords_save_path = '//Users//nitrolichtung//Desktop//scrape_keywords//{}_keywords_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), scrape_language, scrape_mode)
    return keywords_save_path

#Google Trends Search Process
def google_search_process(region, place_name, time_zone, pause_time):
    local_trends_list = []
    search_attempt = TrendReq(hl=region, tz=time_zone, timeout=(5,10), proxies=['http://127.0.0.1:7890'], retries=2, backoff_factor=pause_time)
    local_trends = search_attempt.trending_searches(pn=place_name)
    trends_values = local_trends.values.tolist()
    loacl_trends_list = []
    for value in trends_values:
        item = str(value[0])
        if item.isspace()==False and len(item.strip('\n'))>0:
            item = item.replace('   ', '')
            item = item.replace('\'', '')
        else:
            continue
        local_trends_list.append(item)
    return local_trends_list

#Google Translate Process
def google_translate_process(translate_text, translate_language):
    translator = google_translator(url_suffix='cn', timeout=5)
    translator_result = translator.translate(text=translate_text, lang_tgt=translate_language)
    return translator_result

def save_keywords(keyword_list, target_path):
    with codecs.open(target_path, mode='w', encoding='utf-8') as target_keywords:
        for keyword in keyword_list:
            target_keywords.write(keyword + '\n')

#Create Specific Keywords
specific_keyword_list = []
with codecs.open(keywords_path, mode='r', encoding='utf-8') as specific_keywords:
    for specific_keyword in specific_keywords:
        if specific_keyword.isspace()==False and len(specific_keyword.strip('\n'))>0:
            specific_keyword_list.append(specific_keyword.strip('\n'))
        else:
            pass

#Write Universal Keywords
english_universal_keyword_list = google_search_process('en-UK', 'united_kingdom', '60', scrape_pause_time)
pidgin_universal_keyword_list = google_search_process('ha-NG', 'nigeria', '60', scrape_pause_time)
french_universal_keyword_list = google_search_process('fr-FR', 'france', '60', scrape_pause_time)
hausa_universal_keyword_list = []

for universal_keyword in pidgin_universal_keyword_list:
    hausa_universal_keyword = google_translate_process(universal_keyword, 'ha')
    hausa_universal_keyword_list.append(hausa_universal_keyword)

english_universal_path = generate_keywords_path('en', 'trends')
save_keywords(english_universal_keyword_list, english_universal_path) #Save English Universal Keywords

french_universal_path = generate_keywords_path('fr', 'trends')
save_keywords(french_universal_keyword_list, french_universal_path) #Save English Universal Keywords

pidgin_universal_path = generate_keywords_path('pidgin', 'trends')
save_keywords(pidgin_universal_keyword_list, pidgin_universal_path) #Save Pidgin Specific Keywords

hausa_universal_path = generate_keywords_path('ha', 'trends')
save_keywords(hausa_universal_keyword_list, hausa_universal_path) #Save Hausa Specific Keywords

#Write Specific Keywords
if specific_keyword_list == []:
    pass
else:
    english_specific_path = generate_keywords_path('en', 's')
    save_keywords(specific_keyword_list, english_specific_path) #Save English Specific Keywords

    french_specific_path = generate_keywords_path('fr', 's')
    save_keywords(specific_keyword_list, french_specific_path) #Save French Specific Keywords

    pidgin_specific_path = generate_keywords_path('pidgin', 's')
    save_keywords(specific_keyword_list, pidgin_specific_path) #Save Pidgin Specific Keywords

    hausa_specific_path = generate_keywords_path('ha', 's')
    with codecs.open(hausa_specific_path, mode='w', encoding='utf-8') as hausa_specific_keywords:
        for hausa_specific_keyword in specific_keyword_list:
            hausa_specific_keyword = google_translate_process(hausa_specific_keyword, 'ha')
            hausa_specific_keywords.write(hausa_specific_keyword + '\n') #Save Hausa Specific Keywords