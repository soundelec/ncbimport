import os, pandas, time
from slugify import slugify
from functions import *

fh = open('languages.tmp', 'w')
with open('ncb18.txt') as skedfile:
    for line in skedfile:
        freq = (line[0:5].strip())
        mw = (is_freq_mw(freq))
        if mw == True:
            pass # ignore line if frequency is in the MW band
        if mw == False:
            lang = line[56:82] # extract name of language
            lang = single_lang(lang) # take extra info off end of language string
            if lang == "":
                pass
            else:
                fh.write(lang + '\n') # write to file with new line at end
fh.close()

# We now have a file with all the station names from ncb18.txt but need to deduplicate
lines_seen = set() # create tuple
fh = open('languages.csv', 'w')
with open('languages.tmp') as broadcastersfile:
    for line in broadcastersfile:
        slug = slugify(line)
        if slug not in lines_seen: # not a duplicate
            fh.write(line)
            lines_seen.add(slug) # add to tuple so it will be dropped when encountered again
fh.write("Unknown Language")
fh.close()
os.remove('languages.tmp') # remove original file with dupes

pk = 0
yamlfile = open('languages.yaml', 'w')
with open('languages.csv') as broadcastersfile:
    for line in broadcastersfile:
        language = str(line.strip())
        if language == "":
            pass
        else:
            pk = pk + 1
            yamlfile.write("- model: shortwave.language" + '\n')
            yamlfile.write("  pk: " + str(pk) + '\n')
            yamlfile.write("  fields:" + '\n')
            yamlfile.write("    language: " + language + '\n')
            yamlfile.write("    slug: " + slugify(language) + '\n')
            yamlfile.write('\n')
            print("written language", pk, ": ", language)
