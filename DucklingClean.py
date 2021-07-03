from num2words import num2words
from google_trans_new import google_translator

num=7.5
result=num2words(number=str(num), lang='en')
print(result)

translator = google_translator(url_suffix='cn', timeout=5)
translate_text = translator.translate(result, lang_tgt='ha')  
print(translate_text)