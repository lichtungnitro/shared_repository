import tkinter as tk
from google_trans_new import google_translator

window = tk.Tk()
window.title('Google Tanslate')

lable_url_suffix = tk.Label(window, text='URL Suffix')
lable_url_suffix.pack()
entry_url_suffix = tk.Entry(window, show=None)
entry_url_suffix.pack()

lable_lang_tgt = tk.Label(window, text='Target Language')
lable_lang_tgt.pack()
entry_lang_tgt = tk.Entry(window, show=None)
entry_lang_tgt.pack()

lable_trans_tgt = tk.Label(window, text='Content for Translation')
lable_trans_tgt.pack()
entry_trans_tgt = tk.Entry(window, show=None)
entry_trans_tgt.pack()

def get_entry():
    translator = google_translator(url_suffix=entry_url_suffix.get(), timeout=5)
    translate_text = translator.translate(entry_trans_tgt.get(), lang_tgt=entry_lang_tgt.get())  
    print(translate_text)

print_suffix = tk.Button(window, text='Translate', command=get_entry)
print_suffix.pack()

window.mainloop()

if __name__ == '__main__':
    main()