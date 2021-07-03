import codecs
from os import path, listdir, remove

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
    for char in '!"#$&()*+,./:;<=>?@[\\]^_{|}·~•':
        text = text.replace(char, '')
    return text

#Global Settings
date = '2021-06-27'
lang = 'en'
mode = 'common'
rank = 500
root = '//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//'.format(date, lang, mode)
temporary =  path.join(root, 'temporary_output.txt')
statics_top_rank = path.join(root, 'statics_top.txt')
statics_bot_rank = path.join(root, 'statics_bot.txt')
dictionary = ''

#Get Word Frequency
combine_text(root)
raw_text = get_text(temporary)
words = raw_text.split()
counts = {}
for word in words:
    counts[word] = counts.get(word,0) + 1

items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True)
items_range = len(items)-1

if rank < items_range+1:
    pass
else:
    rank = items_range

#Write Top Rank
with codecs.open(statics_top_rank, mode='a', encoding='utf-8') as s:
    s.write('kwd.      top-rank\n------------------\n')
for counter in range(rank):
    word_t, count_t = items[counter]
    with codecs.open(statics_top_rank, mode='a', encoding='utf-8') as s:
        s.write("{0:<10}{1:>5}".format(word_t, count_t) + '\n')
        
#Write Bottom Rank
with codecs.open(statics_bot_rank, mode='a', encoding='utf-8') as s:
    s.write('kwd.      bot-rank\n------------------\n')
for counter in range(rank):
    word_b, count_b = items[items_range-counter]
    with codecs.open(statics_bot_rank, mode='a', encoding='utf-8') as s:
        s.write("{0:<10}{1:>5}".format(word_b, count_b) + '\n')

#Remove Temporary File
remove(temporary)