# functions.py: generic functions for re-use across the import scripts

def is_freq_mw(freq): # function to detect MW stations as these are not needed
    freq = freq
    freq = int(freq)
    if freq < 2000:
        return True
    else:
        return False

def single_lang(lang): # function to strip extra stuff from end of strings
    slash = '/'
    bracket = '('
    quote = '"'
    lang = lang
    lang = lang.split(slash, 1)[0]
    lang = lang.split(bracket, 1)[0]
    lang = lang.split(quote, 1)[0]
    lang = lang.strip() # strip off white space
    return lang
