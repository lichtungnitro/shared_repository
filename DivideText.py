import codecs
from os import mkdir, path
from tqdm import tqdm

#Settings
divide_date = '2021-06-27'
divide_language = 'en'
divide_target = 'common'
input_path = '//Users//nitrolichtung//Downloads//Movie//twitter_search//{}_desc_clean_{}_{}.txt'.format(divide_date, divide_language, divide_target)
save_path = '//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}'.format(divide_date, divide_language, divide_target) 

#Define Piece Size
file_size = path.getsize(input_path) / float(1024*1024)
divide_pieces = 2 * int(file_size)

#Creating Save Path
try:
    mkdir(save_path)
except Exception as mkdir_error:
    pass

#Divide Original File
origin = codecs.open(input_path, mode='r', encoding='utf-8').readlines()
piece_len = len(origin)//divide_pieces if len(origin)%divide_pieces==0 else len(origin)//divide_pieces+1

for count in tqdm(range(divide_pieces)):
    f = codecs.open('//Users//nitrolichtung//Downloads//Movie//twitter_divided//{}_task_{}_{}//{}_desc_clean_{}_{}_piece_{}.txt'.format(divide_date, divide_language, divide_target, divide_date, divide_language, divide_target, count+1), mode='a', encoding='utf-8')
    f.writelines(origin[count*piece_len:(count+1)*piece_len])
