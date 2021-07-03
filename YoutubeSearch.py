import pretty_errors #Error Package
from youtubesearchpython import VideosSearch #Youtube Search Package
import codecs #Write File Package
from datetime import datetime #Datetime Package
from os import system, listdir, mkdir, path, remove #Use youtube-dl Download Command
from re import compile, sub, IGNORECASE #Regular Expression Package
from pysubparser import parser #Parse SRT Package
from time import sleep #Search Gap Package
from tqdm import tqdm #Process Bar Package

#Scrape Setting
target_language = 'en' #Choosing from en/pidgin/ha
scrape_language = 'en' #Choosing from en/ha
scrape_region = 'US' #Chooding from UK/NG
scrape_mode = 'k' #Choosing from u/s
scrape_repeat_time = 20 #Amount to Scrape
scrape_pause_time = 1 #Pause for Scraper

'''
Scraper Setting Recommendation
#English Scraper:
#Pidgin Scrpaper:
#Hausa Scraper:
'''

#Path for Searched Content
clean_title_path = '//Users//nitrolichtung//Downloads//Movie//youtube_search//{}_title_clean_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
clean_url_path = '//Users//nitrolichtung//Downloads//Movie//youtube_search//{}_url_clean_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
#Path for Searching Keywords
keywords_path = '//Users//nitrolichtung//Desktop//scrape_keywords//{}_keywords_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
#Path for VTT Subtitles
vtt_subtitle_path = '/Users/nitrolichtung/Downloads/Movie'
#Path for SRT Subtitles
srt_subtitle_path = '/Users/nitrolichtung/Downloads/Movie/youtube_subtitle/{}_srt_subtitle_{}_{}'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
#Path for TXT Subtitles
txt_subtitle_path = '/Users/nitrolichtung//Downloads/Movie/youtube_subtitle/{}_txt_subtitle_{}_{}'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)

#Generate Save Path for SRT and TXT Subtitle
try:
    mkdir(srt_subtitle_path)
    mkdir(txt_subtitle_path)
except Exception as mkdir_error:
    pass

#Read Keyword File into List
search_list = []
with codecs.open(keywords_path, mode='r', encoding='utf-8') as keywords:
    for keyword in keywords:
        search_list.append(keyword.strip('\n'))

#Define Scrape Process
def scrape_youtube_info(search_query, scrape_item, repeat_time, sleep_time):
    scrape_result = []
    round = 1
    scrape_attempt = VideosSearch(query=search_query, limit=repeat_time, language=scrape_language, region=scrape_region)
    while round < repeat_time:
        try:
            scrape_result.append(scrape_attempt.result()['result'][round][scrape_item])
        except Exception as append_error:
            pass
        round = round + 1
        sleep(sleep_time)
    return scrape_result

#Define Search Process Bar
process_bar_search = tqdm(total = len(search_list) * 2)

#Scrape Key Information
scrape_title_list = []
scrape_url_list = []

for search_query in search_list:
    scrape_title_list = scrape_title_list + scrape_youtube_info(search_query, 'title', scrape_repeat_time, scrape_pause_time)
    process_bar_search.set_description('searched %s title' % search_query)
    process_bar_search.update(1)
    scrape_url_list = scrape_url_list + scrape_youtube_info(search_query, 'link', scrape_repeat_time, scrape_pause_time)
    process_bar_search.set_description('searched %s url' % search_query)
    process_bar_search.update(1)

process_bar_search.close() #Search Process Complete

#Remove Dulplicate Element in List
def remove_dulplicate(origin_list):
    clean_list = list(set(origin_list))
    clean_list.sort(key=origin_list.index)
    return clean_list

#Remove Dulplicate Title and URL and Save File
with codecs.open(clean_title_path, mode='a', encoding='utf-8') as clean_title_file:
    for clean_title in remove_dulplicate(scrape_title_list):
        if len(clean_title.strip('\n'))>0 and clean_title.isspace()==False:
            clean_title_file.write(clean_title + '\n')
        else:
            continue
print('cleaning {} is complete, check your path:\n{}'.format('title', clean_title_path))

with codecs.open(clean_url_path, mode='a', encoding='utf-8') as clean_url_file:
    for clean_url in remove_dulplicate(scrape_url_list):
        if len(clean_url.strip('\n'))>0 and clean_url.isspace()==False:
            clean_url_file.write(clean_url + '\n')
        else:
            continue
print('cleaning {} is complete, check your path:\n{}'.format('url', clean_url_path))

#Watch Youtube Video and Download Subtitles
with codecs.open(clean_url_path, mode='r', encoding='utf-8') as watch_url_list:
    for watch_url in watch_url_list:
        try:
            system('youtube-dl --write-sub --write-auto-sub --sub-lang {} --no-warnings --continue --skip-download {}'.format(scrape_language, watch_url))
        except Exception as transcribe_error:
            pass

#Convert VTT Subtitles into SRT Ones
convert_vtt_subtitle = []
for check_vtt_subtitle in listdir(vtt_subtitle_path):
    if check_vtt_subtitle[-3:] == 'vtt':
        convert_vtt_subtitle.append(check_vtt_subtitle)
    else:
        continue

#Define Convert Process Bar
process_bar_convert = tqdm(total = len(convert_vtt_subtitle) * 2)

#Convert VTT Subtitles into SRT Ones
for vtt_subtitle in convert_vtt_subtitle:
    space_pattern = compile('\s')
    vtt_pattern = compile('.vtt', IGNORECASE)
    srt_subtitle = vtt_pattern.sub('.srt', vtt_subtitle) 
    normal_srt_subtitle = space_pattern.sub('\\ ', srt_subtitle) #Generate Normal SRT File Name
    normal_vtt_subtitle = space_pattern.sub('\\ ', vtt_subtitle) #Generate Normal VTT File Name
    try:
        system('ffmpeg -i {} {}'.format(path.join(vtt_subtitle_path, normal_vtt_subtitle), path.join(srt_subtitle_path, normal_srt_subtitle)))
    except Exception as convert_error:
        pass
    remove(path.join(vtt_subtitle_path, vtt_subtitle)) #Remove VTT File
    process_bar_convert.update(1)
    process_bar_convert.set_description('converted %s' % srt_subtitle)

#Convert SRT Subtitles into TXT Ones
for convert_srt_subtitle in listdir(srt_subtitle_path):
    srt_lines = parser.parse(path.join(srt_subtitle_path, convert_srt_subtitle), subtitle_type='srt', encoding='utf-8')
    srt_pattern = compile('.srt', IGNORECASE)
    txt_subtitle = srt_pattern.sub('.txt', convert_srt_subtitle) #Generate TXT File Name
    with codecs.open(path.join(txt_subtitle_path, txt_subtitle), mode='w', encoding='utf-8') as txt_file:
        for srt_line in srt_lines:
            txt_file.write(str(srt_line) + '\n')
    process_bar_convert.set_description('converted %s' % txt_subtitle)
    process_bar_convert.update(1)

process_bar_convert.close() #Convert Process Complete
