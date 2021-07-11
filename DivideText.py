import codecs
from os import mkdir, path
from tkinter.constants import W
from tqdm import tqdm
import tkinter as tk
from tkinter import ttk

#Define Run Script
def run_script():
    #Soft Settings
    divide_date = entry_date.get()
    divide_language = combobox_lang.get()
    divide_target = entry_target.get()

    #Hard Settings
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

if __name__ == '__main__':
    #Build Window
    container = tk.Tk()
    container.title('Divide') #Set Title

    label_date = tk.Label(container, text='Divide Date')
    label_date.grid(row=0, column=0, sticky=W)
    default_entry_date = tk.StringVar(value='2000-00-00')
    entry_date = tk.Entry(container, textvariable=default_entry_date)
    entry_date.grid(row=0, column=1) #Set Date

    lable_lang = tk.Label(container, text='Divide Lang')
    lable_lang.grid(row=1, column=0, sticky=W)
    divide_lang_turple = ('en', 'ng', 'ha', 'fr', 'sw')
    slected_lang = tk.StringVar()
    combobox_lang = ttk.Combobox(container, textvariable=slected_lang, width=18)
    combobox_lang['values'] = divide_lang_turple
    combobox_lang.current(0)
    combobox_lang.grid(row=1, column=1) #Set Language

    label_target = tk.Label(container, text='Divide Target')
    label_target.grid(row=2, column=0, sticky=W)
    default_entry_target = tk.StringVar(value='universal')
    entry_target = tk.Entry(container, textvariable=default_entry_target)
    entry_target.grid(row=2, column=1) #Set Target

    #Run Container
    button_run_script = tk.Button(container, text='Run', command=run_script)
    button_run_script.grid(row=3, column=0) #Run Script Button

    button_quit_script = tk.Button(container, text='Quit', command=container.quit)
    button_quit_script.grid(row=3, column=1) #Quit Script Button

    container.mainloop()