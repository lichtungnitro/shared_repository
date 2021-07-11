import codecs
from os import path, listdir, remove
from tkinter.constants import W
import tkinter as tk
from tkinter import ttk

def run_script():
    #Soft Settings
    date = entry_date.get()
    lang = combobox_lang.get()
    mode = entry_target.get()
    rank = int(entry_rank.get())

    #Hard Settings
    root = '//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//'.format(date, lang, mode)
    temporary =  path.join(root, 'temporary_output.txt')
    statics_top_rank = path.join(root, 'statics_top.txt')
    statics_bot_rank = path.join(root, 'statics_bot.txt')
    statics_weird = path.join(root, 'statics_weird.txt')

    #Combine Text Files
    def combine_text(input_path):
        whole_file = [path.join(input_path,file) for file in listdir(input_path)]
        content = []
        for write in whole_file:
            with codecs.open(write, mode='rb') as write_file:
                content = content + write_file.readlines()
        output_path = path.join(input_path, 'temporary_output.txt')
        with open(output_path, mode='wb') as output_file:
            output_file.writelines(content)

    #Get Raw Text
    def get_text(input_file):
        text = codecs.open(input_file, mode='r', errors='ignore', encoding='utf-8').read()
        text = text.lower()
        text = text.replace('<websiteaddress>', '')
        text = text.replace('<numbercollection>', '')
        text = text.replace('<namecollection>', '')
        text = text.replace('<phonecollection>', '')
        text = text.replace('<shorturlcollection>', '')
        text = text.replace('<fullurlcollection>>', '')
        text = text.replace('hashtagtopic', '')
        for char in '!"#$&()*+,./:;<=>?@[\\]^_{|}·~•‘’':
            text = text.replace(char, '')
        return text.strip('\'')

    #Get Word Frequency
    weird_word_list = set()
    combine_text(root)
    raw_text = get_text(temporary)
    words = raw_text.split()
    counts = {}

    #Statics for Weird
    for word in words:
        counts[word] = counts.get(word, 0) + 1
        if counts[word] < 4 and len(word) > 14:
            weird_word_list.add(word)

    #Confirm Items Amount
    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    items_range = len(items)
    if rank < items_range:
        pass
    else:
        rank = items_range

    #Write Top Rank
    for counter in range(rank-1):
        word_t, count_t = items[counter]
        with codecs.open(statics_top_rank, mode='a', encoding='utf-8') as top_rank:
            top_rank.write('{0:<10}{1:>5}'.format(word_t, count_t) + '\n')
            
    #Write Bottom Rank
    for counter in range(rank-1):
        word_b, count_b = items[items_range-counter-1]
        with codecs.open(statics_bot_rank, mode='a', encoding='utf-8') as bot_rank:
            bot_rank.write('{0:<10}{1:>5}'.format(word_b, count_b) + '\n')

    #Write Wired Words
    for weird_word in weird_word_list:
        with codecs.open(statics_weird, mode='a', encoding='utf-8') as weird_file:
            weird_file.write(weird_word + '\n')

    #Remove Temporary File
    remove(temporary)

if __name__ == '__main__':
    #Build Window
    container = tk.Tk()
    container.title('Frequency') #Set Title

    label_date = tk.Label(container, text='Word Date')
    label_date.grid(row=0, column=0, sticky=W)
    default_entry_date = tk.StringVar(value='2000-00-00')
    entry_date = tk.Entry(container, textvariable=default_entry_date)
    entry_date.grid(row=0, column=1) #Set Date

    lable_lang = tk.Label(container, text='Word Lang')
    lable_lang.grid(row=1, column=0, sticky=W)
    divide_lang_turple = ('en', 'ng', 'ha', 'fr', 'sw')
    slected_lang = tk.StringVar()
    combobox_lang = ttk.Combobox(container, textvariable=slected_lang, width=18)
    combobox_lang['values'] = divide_lang_turple
    combobox_lang.current(0)
    combobox_lang.grid(row=1, column=1) #Set Language

    label_target = tk.Label(container, text='Word Target')
    label_target.grid(row=2, column=0, sticky=W)
    default_entry_target = tk.StringVar(value='universal')
    entry_target = tk.Entry(container, textvariable=default_entry_target)
    entry_target.grid(row=2, column=1) #Set Target

    label_rank = tk.Label(container, text='Word Rank')
    label_rank.grid(row=3, column=0, sticky=W)
    default_entry_rank = tk.StringVar(value='500')
    entry_rank = tk.Entry(container, textvariable=default_entry_rank)
    entry_rank.grid(row=3, column=1) #Set Rank

    #Run Container
    button_run_script = tk.Button(container, text='Run', command=run_script)
    button_run_script.grid(row=4, column=0) #Run Script Button

    button_quit_script = tk.Button(container, text='Quit', command=container.quit)
    button_quit_script.grid(row=4, column=1) #Quit Script Button

    container.mainloop()