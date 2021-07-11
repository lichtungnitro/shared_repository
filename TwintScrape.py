from twint import run, Config #Twitter Search Package
import codecs #Write File Package
import pandas #Operate CSV Package
from datetime import datetime #Datetime Package
from re import search, sub, compile, error, IGNORECASE #Regular Expression Package
from emoji import demojize #Demojize Package
from tqdm import tqdm #Process Bar Package
from os import remove #Removal Package
import tkinter as tk #User Interface Package
from tkinter import ttk #Combobox Package
from tkinter.constants import W #Align Package

def run_script():
    #Scrape Setting
    target_language = combobox_target_lang.get() #Choosing from en/pidgin/ha
    scrape_language = combobox_scrape_lang.get() #Choosing from en/in
    scrape_region = entry_region.lower() #Choosing from lagos/london
    scrape_mode = entry_target.get() #Choosing from u/s
    scrape_repeat_time = int(entry_limit.get()) #Amount to Scrape
    #scrape_pause_time = 1 #Pause for Scraper
    #scrape_since_date = '2019-01-01 08:15:27'
    #scrape_until_date = '2019-01-01 08:15:27'
    #scrape_year = 2020

    #Path for Searched Content
    save_content_path = '//Users//nitrolichtung//Downloads//Movie//twitter_search//{}_content_{}_{}.csv'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
    save_desc_path = '//Users//nitrolichtung//Downloads//Movie//twitter_search//{}_desc_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
    clean_desc_path = '//Users//nitrolichtung//Downloads//Movie//twitter_search//{}_desc_clean_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)

    #Path for Searching Keywords
    keywords_path = '//Users//nitrolichtung//Desktop//scrape_keywords//{}_keywords_{}_{}.txt'.format(datetime.now().strftime('%Y-%m-%d'), target_language, scrape_mode)
    temporary_path = '//Users//nitrolichtung//Desktop//twint_counter.txt'

    c = Config() #Set Up Config

    #Scrape Config
    c.Near = scrape_region #Near Certain City
    c.Lang = scrape_language #Compatible Language
    c.Limit = scrape_repeat_time #Number of Tweets to Pull
    c.Popular_tweets = False #Scrape Popular Tweet Rather Than Recent Ones
    c.Filter_retweets = False #Exclude Retweets
    c.Count = True #Count Total Numver of Tweets Fetched
    c.Hide_output = False #Hide Output
    c.Show_hashtags = True #Show Hashtags
    c.Retries_count = 5 #Retries Count

    #Specific Scrape Config
    #c.Email = True #Contains Email
    #c.Phone = True # Contains Phone
    #c.Links = 'include' #Include or Exclude Links

    #Scrape Time Config

    #c.Since = scrape_since_date #Since Time
    #c.Since = scrape_until_time #Until Time
    #c.Year = scrape_year #Scrape Year

    #Proxy Config
    c.Proxy_host = '127.0.0.1' #Proxy Hostname or IP
    c.Proxy_port = 9999 #Proxy Port
    c.Proxy_type = 'http' #Proxy Type

    #Save Config
    c.Lowercase = True #Convert Uppercases into Lowercases
    c.Store_csv = True #Write as CSV File
    c.Output = save_content_path #Name of Output File

    #Read Keyword File into List
    search_list = []
    with codecs.open(keywords_path, mode='r', encoding='utf-8') as keywords:
        for keyword in keywords:
            search_list.append(keyword.strip('\n'))
    remove_dulpicate_search_list = list(set(search_list))

    #Define Search Process Bar
    process_bar_search = tqdm(total = len(search_list))

    #Seach and Save Texts
    for search_query in remove_dulpicate_search_list:
        c.Search = search_query #Search Terms
        try:
            run.Search(c)
            with codecs.open(temporary_path, mode='w', encoding='utf-8') as temporary:
                temporary.write(f'file name: {save_content_path}\nlatest searching: {search_query}')
        except Exception as twint_search_error:
            print(twint_search_error)
            continue  #Run Search
        process_bar_search.set_description('searched %s content' % search_query)
        process_bar_search.update(1) #Update Search Bar

    process_bar_search.close() #Search Process Complete

    #Save Desc File
    df_content = pandas.read_csv(save_content_path, error_bad_lines=False, dtype='unicode', low_memory=False)
    df_content['tweet'].to_csv(save_desc_path, index=False, header=None, encoding='utf_8_sig')

    #Clean Files and Process Empty, Website, Commet, Topic and Emoji Lines
    def clean_text_file(save_path, clean_path, content_path, entity):
        url_pattern = compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'\
            , IGNORECASE) #Define URL Pattern
        comment_pattern = compile(r'@\S*?\s') #Define Comment Pattern
        topic_pattern = compile(r'#\S*?\s') #Define Topic Pattern
        emoji_pattern = compile(r':\S*?:') #Define Other Emoji Pattern

        with codecs.open(save_path, mode='r', encoding='utf-8') as save_file:
            for line in save_file:
                line = sub(url_pattern, ' <WebsiteAddress> ', line)
                line = sub(comment_pattern, '[AtUserName]', line)
                #line = sub(topic_pattern, '[HashtagTopic]', line)
                line = demojize(line)
                line = sub(emoji_pattern, '', line)

                if len(line.strip())>0:
                    #and line.strip('\n')) not in clean_lines #Remove Dulpicates
                    try:
                        with codecs.open(clean_path, mode='a', encoding='utf-8') as clean_file:
                            clean_file.write(line.strip() + '\n')
                            print(f'now appending: {line.strip()}')
                    except Exception as clean_line_error:
                        continue
                else:
                    print('now appending: line pass')
                    continue

        remove(save_path) #Remove Save File
        remove(content_path) #Remove Content File
        print('cleaning {} is complete, check your path:\n{}'.format(entity, clean_path))

    #Clean Desc File
    clean_text_file(save_desc_path, clean_desc_path, save_content_path, 'content') #Takes Too Much Time
    try:
        remove(temporary_path)
    except Exception as removal_error:
        pass

if __name__ == '__main__':
    #Build Window
    container = tk.Tk()
    container.title('Scrape') #Set Title

    lable_target_lang = tk.Label(container, text='Target Lang')
    lable_target_lang.grid(row=0, column=0, sticky=W)
    divide_target_lang_turple = ('en', 'ng', 'ha', 'fr', 'sw')
    slected_target_lang = tk.StringVar()
    combobox_target_lang = ttk.Combobox(container, textvariable=slected_target_lang, width=18)
    combobox_target_lang['values'] = divide_target_lang_turple
    combobox_target_lang.current(0)
    combobox_target_lang.grid(row=0, column=1) #Set Target Language

    lable_scrape_lang = tk.Label(container, text='Scrape Lang')
    lable_scrape_lang.grid(row=1, column=0, sticky=W)
    divide_scrape_lang_turple = ('en', 'ha', 'fr', 'sw')
    slected_scrape_lang = tk.StringVar()
    combobox_scrape_lang = ttk.Combobox(container, textvariable=slected_scrape_lang, width=18)
    combobox_scrape_lang['values'] = divide_scrape_lang_turple
    combobox_scrape_lang.current(0)
    combobox_scrape_lang.grid(row=1, column=1) #Set Scrape Language

    label_region = tk.Label(container, text='Scrape Region')
    label_region.grid(row=2, column=0, sticky=W)
    default_entry_region = tk.StringVar(value='lagos')
    entry_region = tk.Entry(container, textvariable=default_entry_region)
    entry_region.grid(row=2, column=1) #Set Scrape Region

    label_target = tk.Label(container, text='Scrape Target')
    label_target.grid(row=3, column=0, sticky=W)
    default_entry_target = tk.StringVar(value='universal')
    entry_target = tk.Entry(container, textvariable=default_entry_target)
    entry_target.grid(row=3, column=1) #Set Scrape Target

    label_limit = tk.Label(container, text='Scrape Limit')
    label_limit.grid(row=4, column=0, sticky=W)
    default_entry_limit = tk.StringVar(value='1000')
    entry_limit = tk.Entry(container, textvariable=default_entry_limit)
    entry_limit.grid(row=4, column=1) #Set Scrape Limit

    #Run Container
    button_run_script = tk.Button(container, text='Run', command=run_script)
    button_run_script.grid(row=5, column=0) #Run Script Button

    button_quit_script = tk.Button(container, text='Quit', command=container.quit)
    button_quit_script.grid(row=5, column=1) #Quit Script Button

    container.mainloop()