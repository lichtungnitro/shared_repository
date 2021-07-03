import codecs
from os import mkdir
from tqdm import tqdm

#Settings
divide_date = '2021-06-08'
divide_language = 'fr'
divide_target = 'time'
divide_pieces = 11


generate_
input_path = '//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//{}_desc_identified_{}_{}_'.format(divide_date, divide_language, divide_target) 

with codecs.open

#Divide Original File
origin = codecs.open(input_path, mode='r', encoding='utf-8').readlines()
piece_len = len(origin)//divide_pieces if len(origin)%divide_pieces==0 else len(origin)//divide_pieces+1

for count in tqdm(range(divide_pieces)):
    f = codecs.open('//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//{}_desc_clean_{}_{}_piece_{}.txt'.format(divide_date, divide_language, divide_target, divide_date, divide_language, divide_target, count+1), mode='a', encoding='utf-8')
    f.writelines(origin[count*piece_len:(count+1)*piece_len])
