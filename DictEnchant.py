from spellchecker import SpellChecker
spell = SpellChecker(language='en')

# find those words that may be misspelled
misspelled = spell.unknown(['somethiing', 'is', 'hapenning', 'google'])

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))