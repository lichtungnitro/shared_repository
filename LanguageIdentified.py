import codecs #Write File Package
from fasttext import load_model #Indentifier Package
from tqdm import tqdm #Process Bar Package
from subprocess import check_output, STDOUT #Use echo Translate Package
from re import sub, compile, search, findall, finditer, IGNORECASE #Regular Expression Package
from num2words import num2words #Number to Words Package
from google_trans_new import google_translator #Google Translation Package
from os import remove, path #Remove Original Package
from glob import glob #Count File Number Package
from emoji import demojize #Demojize Package
from json import load #Concatenate Built-in Package
from random import choice #Random List Value Package
from faker import Faker #Fake Entity Package

#Soft Setting
clean_language = 'ha'
clean_number = 'ha' 
target_language_dict = {'fr':['fr'],
                        'en':['en'],
                        'sw':['sw'],
                        'pidgin':['Nigerian Pidgin(pcm)'],
                        'ha':['hua_NG', 'hau_NE', 'Tonga (Zambia) (toi)', 'Somali (som)', 'Soninke (snk)', 'Chamorro (cha)', 'Fijian (fij)', 'Turkish (tur)', 'Lozi (loz)']
                        }
clean_date = '2021-06-16'
clean_target = 'novel'
clean_start_piece = 52
clean_threshold = 0.6
clean_maximum_word_len = 15
clean_maximum_query_len = 1000

#Hard setting
clean_minimum_query_len = 2
clean_proxies = {'http':'127.0.0.1:7890'}

#Model Path
pretrained_model_path = '//Users//nitrolichtung//Desktop//language_lib//lid.176.bin'
dictionary_path = '//Users//nitrolichtung//Documents//Repository//witch_language_master//langid.py'
built_in_dictionary_path = '//Users//nitrolichtung//Desktop//language_lib//language-built-in-dict'
fake_name_path = '//Users//nitrolichtung//Desktop//language_lib//language-built-in-dict'

#Read and Save Path
save_path = '//Users//nitrolichtung//Desktop//collection//{}_{}_collection_{}.txt'.format(clean_date, clean_target, clean_language)

#Google Translate Process
def generate_path(mode, counter):
    read_path = '//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//{}_desc_{}_{}_{}_piece_{}.txt'.format(clean_date, clean_language, clean_target, clean_date, mode, clean_language, clean_target, counter+1)
    return read_path

#Clean Piece Number
clean_piece = len(glob('//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//*_clean_*.txt'.format(clean_date, clean_language, clean_target)) +\
                glob('//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//*_tocheck_*.txt'.format(clean_date, clean_language, clean_target)))

#Translated Number
def google_translate_process(translate_text, translate_language):
    translator = google_translator(url_suffix='cn', timeout=5, proxies=clean_proxies)
    translator_result = translator.translate(text=translate_text, lang_src='en', lang_tgt=translate_language)
    return translator_result

#Concatenate Built-in Dictionary
def concat_built_in_content(root, dict_name, dict_lang, dict_format):
    entity_list = []
    with codecs.open(path.join(root, f'{dict_name}_{dict_lang}.{dict_format}'), mode='r', encoding='utf-8') as built_in:
        if dict_format == 'json':
            entity_dict = load(built_in)
            return entity_dict
        elif dict_format == 'txt':
            for entity in built_in:
                entity_list.append(str(entity))
            return entity_list

#Language Identified
def identify_language(sentences):
    predict_lang_list = []
    sentences = [sentence.strip() for sentence in sentences if sentence.strip() != '']
    if clean_language != 'ha':
        model = load_model(pretrained_model_path)
        for num in range(len(sentences)):
            try:
                predict_result = model.predict(sentences)[0][num][0]
                predict_result = predict_result.replace('__label__', '')
                predict_lang_list.append(predict_result)
                print('[ {} ] predicted result -> [ {} ]'.format(sentences[num], predict_result))
            except Exception as predict_error:
                predict_lang_list.append('null')
                pass
            num = num + 1
    elif clean_language == 'ha':
        for sentence in sentences:
            command = 'echo "{}" | python3 {}'.format(sentence, dictionary_path)
            try:
                result = str(check_output(command, stderr=STDOUT, timeout=5, shell=True)).replace('\\n', '\n')
                result = result.replace(': ', ':')
                position = result.find('Top 10 Guesses')
                result = result[position+16:].split('\n')[0].split(':')
                if len(result)<2:
                    result =  ['null', 1]
                else:
                    pass
            except Exception as clean_error:
                result =  ['null', 1]
                pass
            if float(result[1])>clean_threshold:
                predict_result = result[0]
                predict_lang_list.append(predict_result)
                print('[ {} ] predicted result -> [ {} ]'.format(sentence, predict_result))
            else:
                predict_result = 'null'
                predict_lang_list.append(predict_result)
    return predict_lang_list

#Phone Number Dict
duel_phone_replace_dict_en = concat_built_in_content(built_in_dictionary_path, 'dueldigitnumcollection', 'en', 'json')
duel_phone_replace_dict_ha = concat_built_in_content(built_in_dictionary_path, 'dueldigitnumcollection', 'ha', 'json')
duel_phone_replace_dict_fr = concat_built_in_content(built_in_dictionary_path, 'dueldigitnumcollection', 'fr', 'json')
duel_phone_replace_dict_sw = concat_built_in_content(built_in_dictionary_path, 'dueldigitnumcollection', 'sw', 'json')
single_phone_replace_dict_en = concat_built_in_content(built_in_dictionary_path, 'singledigitnumcollection', 'en', 'json')
single_phone_replace_dict_ha = concat_built_in_content(built_in_dictionary_path, 'singledigitnumcollection', 'ha', 'json')
single_phone_replace_dict_fr = concat_built_in_content(built_in_dictionary_path, 'singledigitnumcollection', 'fr', 'json')
single_phone_replace_dict_sw = concat_built_in_content(built_in_dictionary_path, 'singledigitnumcollection', 'sw', 'json')

#Fake Name Entity
def fake_name(faker_lang):
    if faker_lang == 'fr':
        faker = Faker(locale='fr_FR')
        fake_name = faker.name()
    elif faker_lang == 'en':
        faker = Faker(locale='en_US')
        fake_name = faker.name()
    else:
        fake_name = choice(concat_built_in_content(built_in_dictionary_path, 'namecollection', faker_lang, 'txt')).rstrip()
    return fake_name


#Define Clean Pattern
short_url_pattern = compile(r'https://t.co/[\s\S]{10}')
cn_pattern = compile(u'[\u4e00-\u9fff]+') #Chinese
kr_pattern = compile(u'[\uac00-\ud7ff]+') #Korean
jp_kat_pattern = compile(u'[\u30a0-\u30ff]+') #Japanese Kat
jp_hir_pattern = compile(u'[\u3040-\u309f]+') #Japanese Hir
ab_pattern = compile(u'[\u0600-\u06ff]+') #Arabic
ab_cpl_pattern = compile(u'[\u0750-\u077f]+') #Arabic Complement
vg_pattern = compile(u'[\u0900-\u097f]+') #Visagar
symbol_pattern = compile(u"[_^()\"@#|~{}]|[——！\\\\，。、：“”《》\[\]【】￥……«»☆• ⃣]+")
long_url_pattern = compile(u'[a-zA-Z]+://[^\s]*')
email_pattern = compile(u'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
latin_pattern = compile(u'[á|ä|ã|å|ā|Á|Ä|Ã|Å|Ā|ē|ė|ę|Ē|Ė|Ę|ì|į|ī|í|Ì|Į|Ī|Í|õ|ō|ø|ó|ò|ö|Õ|Ō|Ø|Ó|Ò|Ö|ū|ú|Ū|Ú|ć|č|Ć|Č|ł|Ł|ń|ñ|Ń|Ñ|ś|š|Ś|Š|ž|ź|ż|Ž|Ź|Ż]+') #Latin
emoji_pattern = compile(r':\S*?:') #Emoji
url_pattern = compile(
r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'\
    , IGNORECASE) #URL

#Define Number Clean Function
def number_to_words(query):
    #Clean Main Number Detected
    number_list = findall(r'[(\-|\+)\d+(\.\d+)]+', str(query))
    if number_list is None:
        pass
    else:
        for number in number_list:
            if len(str(number.strip('\.\+\-\ ')))<5:
                try:
                    if clean_language == 'en' or clean_language == 'fr':
                        query = str(query).replace(number, ' <{}><{}> '.format(num2words(number=str(number),lang=clean_number), 'NumberCollection'), 1)
                    elif clean_language == 'ha' or clean_language == 'sw':
                        query = str(query).replace(number, ' <{}><{}> '.format(google_translate_process(num2words(number=str(number),lang='en'), clean_number), 'NumberCollection'), 1)
                except Exception as convert_error:
                    continue

            if len(str(number.strip('\.\+\-\ ')))>4:
                if clean_language == 'en':
                    for duel_k, duel_v in duel_phone_replace_dict_en.items():
                        trans_phone = str(number).replace(duel_k, duel_v)
                    for single_k, single_v in single_phone_replace_dict_en.items():
                        trans_phone = trans_phone.replace(single_k, single_v)
                elif clean_language == 'ha':
                    for duel_k, duel_v in duel_phone_replace_dict_ha.items():
                        trans_phone = str(number).replace(duel_k, duel_v)
                    for single_k, single_v in single_phone_replace_dict_ha.items():
                        trans_phone = trans_phone.replace(single_k, single_v)
                elif clean_language == 'sw':
                    for duel_k, duel_v in duel_phone_replace_dict_sw.items():
                        trans_phone = str(number).replace(duel_k, duel_v)
                    for single_k, single_v in single_phone_replace_dict_sw.items():
                        trans_phone = trans_phone.replace(single_k, single_v)
                elif clean_language == 'fr' and len(str(number.strip('\.\+\-\ ')))%2 == 0: #French Read Even Number
                    trans_phone = ''
                    for count_even in range(int(len(str(number.strip('\.\+\-\ ')))/2)):
                        try:
                            trans_phone = trans_phone + ' ' + duel_phone_replace_dict_fr[str(number.strip('\.\+\-\ '))[2*count_even:2*count_even+2]]
                            count_even = count_even + 1
                        except Exception as trans_fr_phone_error:
                            count_even = count_even + 1
                            continue
                        trans_phone = trans_phone.replace('\.', single_phone_replace_dict_fr['.'])
                elif clean_language == 'fr' and len(str(number.strip('\.\+\-\ ')))%2 != 0: #French Read Odd Number
                    for single_k, single_v in single_phone_replace_dict_fr.items():
                        trans_phone = str(number).replace(single_k, single_v)
                    for count_odd in range(int((len(str(number.strip('\.\+\-\ ')))-1)/2)):
                        try:
                            trans_phone = trans_phone + ' ' + duel_phone_replace_dict_fr[str(number.strip('\.\+\-\ '))[2*count_odd+1:2*count_odd+3]]
                            count_odd = count_odd + 1
                        except Exception as trans_fr_phone_error:
                            count_odd = count_odd + 1
                            continue
                query = str(query).replace(str(number), ' <{}><{}> '.format(trans_phone, 'phonecollection'), 1)
    
    #Clean Raw Number Undetected
    raw_number_list = findall(r'\d+', str(query))
    if raw_number_list is None:
        pass
    else:
        for raw_number in raw_number_list:
            if clean_language == 'en' or clean_language == 'fr':
                query = query.replace(raw_number, ' <{}><{}> '.format(num2words(number=str(raw_number),lang=clean_number), 'NumberCollection'), 1)
            elif clean_language == 'ha' or clean_language == 'sw':
                query = query.replace(raw_number, ' <{}><{}> '.format(google_translate_process(num2words(number=str(raw_number),lang='en'), clean_number), 'NumberCollection'), 1)
    
    #Remove Unnecessary Symbol
    query = sub(r'\<+', '<', str(query))
    query = sub(r'\>+', '>', query)
    return query

def clean_duel_target(raw, single):
    duel_count = 1
    duel_count_space = 1
    duel = '<{}><{}>'.format(single, single)
    duel_spcae_split ='<{}> <{}>'.format(single, single)
    for duel_count in range(2*str(raw).count(duel)):
        raw = str(raw).replace(duel, f'<{single}>')
        duel_count = duel_count + 1
    for duel_count_space in range(2*raw.count(duel_spcae_split)):
        raw = raw.replace(duel_spcae_split, f'<{single}>')
        duel_count_space = duel_count_space + 1
    return raw

#Define High Frequency Replacement
high_freq_dict = {'fr' : concat_built_in_content(built_in_dictionary_path, 'highfreqreplace', 'fr', 'json'),
                'en' : concat_built_in_content(built_in_dictionary_path, 'highfreqreplace', 'en', 'json'),
                'ha' : concat_built_in_content(built_in_dictionary_path, 'highfreqreplace', 'ha', 'json'),
                'ha' : concat_built_in_content(built_in_dictionary_path, 'highfreqreplace', 'sw', 'json')
                }

#Define URL Prefix
url_prefix_dict = {'fr' : ['w w w point ', 'triple w point ', ''],
                'en' : ['w w w dot ', 'triple w dot ', ''],
                'ha' : ['w w w digo ', 'sau uku w digo ', ''],
                'sw' : ['w w w dukta ', 'mara tatu w dukta ', '']
                }

#Define High Frequency Replacement
def high_freq_replace(query, lang):
    rep_dict = high_freq_dict[lang]
    if len(rep_dict) == 0:
        pass
    else:
        for high_key, high_value in rep_dict.items():
            try:
                query = str(query).replace(f' {high_key} ', f' {high_value} ')
            except Exception as high_freq_error:
                pass
    return query

#Define Multiple Repeated Letters of Phrases
def repeated_express_replace(query): #Removing Repeated Letter
    if bool(search(r'((\w)\2{3,})', str(query))):
        for single_match in finditer(r'((\w)\2{3,})', str(query)):
            query = str(query)[:single_match.start()+1] + str(query)[single_match.end():]
    else:
        pass
    if bool(search(r'((\w\w)\2{3,})', str(query))): #Removing Repeated Phrases
        for duel_match in finditer(r'((\w\w)\2{3,})', str(query)):
            query = str(query)[:duel_match.start()+2] + str(query)[duel_match.end():]
    else:
        pass
    return query

#Judge
def judge_long_word(input_query, max_length):
    word_flag = False
    word_set = input_query.split(' ')
    for word in word_set:
        if len(word) > max_length-1:
            word_flag = True
            break
        else:
            pass
    return word_flag


#Generate Language Prediction
for piece_count in tqdm(range(clean_start_piece,clean_piece)):
    
    #Recover Settings
    check_sentences = []
    split_sentences = []

    #Load and Clean Lines
    with codecs.open(generate_path(mode='clean', counter=piece_count), mode='r', encoding='utf-8', errors='ignore') as lines:
        for line in lines:
            line = line.replace('[HashtagTopic]', '') #Clean Hashtag
            line = str(line).replace('[AtUserName]', ' <NameCollection> ') #Replace Name
            line = sub(short_url_pattern, ' <ShortURLCollection> ', line) #Exract URLs
            line = sub(email_pattern, ' <EmailCollection> ', line) #Extract Long URLs 
            line = sub(long_url_pattern, ' <FullURLCollection> ', line) #Extract Long URLs
            line = sub(symbol_pattern, '', line) #Clean Symbols
            line = demojize(line)
            line = sub(emoji_pattern, '', line) #Clean Emoji
            line = sub(url_pattern, ' <websiteaddress> ', line) #Clean URLs
            line = line.replace(' amp;', '')
            if clean_language == 'en':
                line = line.replace('&', ' and ') #Replace And
                line = line.replace('=', ' equal to ') #Replace Equal
                line = line.replace('+', ' plus ') #Replace Plus
            elif clean_language == 'ha':
                line = line.replace('&', ' kama ') 
                line = line.replace('=', ' daidai yake da ')
                line = line.replace('+', ' kara ')
            elif clean_language == 'fr':
                line = line.replace('&', ' et ') 
                line = line.replace('=', ' égale ')
                line = line.replace('+', ' plus ')
            elif clean_language == 'sw':
                line = line.replace('&', ' na ') 
                line = line.replace('=', ' sawa ')
                line = line.replace('+', ' pamoja ')

            #Clean Phone Numbers
            preprocess_list = findall(r'[\d+(\-{1}|\ {1})\d+]+', line)
            sub_list = []
            for sub_word in preprocess_list:
                if len(sub_word)>4:
                    sub_list.append(sub_word)
            if sub_list == []:
                line = str(line)
            else:
                for preprocess in sub_list:
                    line = line.replace(preprocess[1:-1], sub(r'\-', '', preprocess[1:-1])) #Clean Hiven
                    line = line.replace(preprocess[1:-1], sub(r'\ ', '', preprocess[1:-1])) #Clean Space
            line = line.replace('%', 'percent ') #Replace percent
            line = line.replace(':', ' ') #Replace Colon
            line = sub(r'\!+', '!', line) #Clean Unnecessary Exclamation
            line = sub(r'\?+', '?', line) #Clean Unnecessary Question
            line = sub(r'\.+', '.', line) #Clean Unnecessary Dot
            line = sub(r'\*+', '*', line)
            line = sub(r'\*', ' * ', line) #Clean Unnecessary Asterisk
            if bool(search(cn_pattern, line)) or\
                bool(search(kr_pattern, line)) or\
                bool(search(jp_kat_pattern, line)) or\
                bool(search(jp_hir_pattern, line)) or\
                bool(search(ab_pattern, line)) or\
                bool(search(ab_cpl_pattern, line)) or\
                bool(search(vg_pattern, line)) or\
                bool(search(latin_pattern, line)) or\
                not '\n' in line or\
                ' gt;' in line or\
                ' lt;' in line or\
                len(line) < clean_minimum_query_len + 1 or\
                len(line) > clean_maximum_query_len -1 or\
                judge_long_word(line, clean_maximum_word_len):
                #line in check_sentences:
                pass
            elif '\n' in line:
                split_sentences = split_sentences + line.split('\n')
            else:
                line = sub(r' +', ' ', number_to_words(line)) #Translate Number
                line = clean_duel_target(line.lower(), 'namecollection') #Lower Texts
                line = clean_duel_target(line, 'websiteaddress') #Clean Multiple Targets
                line = high_freq_replace(line, clean_language) #Replace High Requency Words
                line = repeated_express_replace(line) #Replace Repeated Letters or Phrases
                check_sentences.append(line.rstrip('\ \.\?\!') + '\n\n')
            
    #Check Splitted Sentences
    for split in split_sentences:
        if bool(search(cn_pattern, split)) or\
            bool(search(kr_pattern, split)) or\
            bool(search(jp_kat_pattern, split)) or\
            bool(search(jp_hir_pattern, split)) or\
            bool(search(ab_pattern, split)) or\
            bool(search(ab_cpl_pattern, split)) or\
            bool(search(vg_pattern, split)) or\
            bool(search(latin_pattern, split)) or\
            ' gt;' in split or\
            ' lt;' in split or\
            len(split) < clean_minimum_query_len + 1 or\
            len(split) > clean_maximum_query_len -1 or\
            judge_long_word(split, clean_maximum_word_len):
            #split in check_sentences:
            pass
        else:
            split = sub(r' +', ' ', number_to_words(split)) #Translate Split
            split = clean_duel_target(split.lower(), 'namecollection') #Lower Texts
            split = clean_duel_target(split, 'websiteaddress') #Clean Multiple Targets
            split = high_freq_replace(split, clean_language) #Replace High Requency Words
            split = repeated_express_replace(split) #Replace Repeated Letters or Phrases
            check_sentences.append(split.rstrip('\ \.\?\!') + '\n\n')

    #Generate Predictions
    predict_list = list(zip(check_sentences, identify_language(check_sentences)))

    #Save Lines
    with codecs.open(generate_path(mode='indentified', counter=piece_count), mode='a', encoding='utf-8') as file:
        for predict in predict_list:
            if predict[1] in target_language_dict[clean_language]:
                file.write(predict[0])
                with codecs.open(generate_path(mode='tocheck', counter=piece_count), mode='a', encoding='utf-8') as check:
                    if '<namecollection>' in predict[0]:
                        random_fake_name = str(fake_name(clean_language)).replace('-', ' ')
                        tocheck = str(predict[0]).replace('<namecollection>', random_fake_name)
                        with codecs.open(path.join(fake_name_path, f'fakerscollection_{clean_language}.txt'), mode='a', encoding='utf-8') as fakefile:
                            fake_name_pieces = random_fake_name.split(' ')
                            for fake_name_piece in fake_name_pieces:
                                fakefile.write(fake_name_piece + '\n')    
                    else:
                        tocheck = str(predict[0])
                    tocheck = tocheck.replace('<websiteaddress>', choice(url_prefix_dict[clean_language]) + choice(concat_built_in_content(built_in_dictionary_path, 'urlcollection', clean_language, 'txt')).rstrip())
                    tocheck = tocheck.replace('<numbercollection>', '')
                    tocheck = tocheck.replace('<phonecollection>', '')
                    tocheck = tocheck.replace('<shorturlcollection>', choice(concat_built_in_content(built_in_dictionary_path, 'urlcollection', clean_language, 'txt')).rstrip())
                    tocheck = tocheck.replace('<fullurlcollection>>', choice(url_prefix_dict[clean_language]) + choice(concat_built_in_content(built_in_dictionary_path, 'urlcollection', clean_language, 'txt')).rstrip())
                    tocheck = tocheck.replace('<', '')
                    tocheck = tocheck.replace('>', '')
                    check.write(tocheck.lstrip())
            else:
                pass

    remove(generate_path(mode='clean', counter=piece_count)) #Remove Original Files

#Remove Dulplicate Fake Names
fake_names_set = set()
with codecs.open(path.join(fake_name_path, f'fakerscollection_{clean_language}.txt'), mode='r', encoding='utf-8') as faker_ents:
    for faker_ent in faker_ents:
        fake_names_set.add(faker_ent)
with codecs.open(path.join(fake_name_path, f'fakenamecollection_{clean_language}.txt'), mode='w', encoding='utf-8') as faker_names:
    for fake_name in fake_names_set:
        faker_names.write(fake_name)
remove(path.join(fake_name_path, f'fakerscollection_{clean_language}.txt')) #Remove Original Fakers
