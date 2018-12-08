import os, pandas, time
from slugify import slugify
from functions import *

fh = open('broadcasters.tmp', 'w')
with open('ncb18.txt') as skedfile:
    for line in skedfile:
        freq = (line[0:5].strip())
        mw = (is_freq_mw(freq))
        if mw == True:
            pass # ignore line if frequency is in the MW band
        if mw == False:
            broadcaster = line[6:37] # extract broadcaster name
            broadcaster = broadcaster.strip() # strip off white space
            if broadcaster == "":
                pass
            else:
                fh.write(broadcaster + '\n') # write to file with new line at end
fh.close()

# We now have a file with all the station names from ncb18.txt but need to deduplicate
lines_seen = set() # create tuple
fh = open('broadcasters.csv', 'w')
with open('broadcasters.tmp') as broadcastersfile:
    for line in broadcastersfile:
        slug = slugify(line)
        if slug not in lines_seen: # not a duplicate
            fh.write(line)
            lines_seen.add(slug) # add to tuple so it will be dropped when encountered again
fh.write("Unknown Broadcaster") # dummy line for blank broadcasters
fh.close()
os.remove('broadcasters.tmp') # remove original file with dupes

pk = 0
yamlfile = open('broadcasters.yaml', 'w')
with open('broadcasters.csv') as broadcastersfile:
    for line in broadcastersfile:
        broadcaster = str(line.strip())
        pk = pk + 1
        yamlfile.write("- model: shortwave.broadcaster" + '\n')
        yamlfile.write("  pk: " + str(pk) + '\n')
        yamlfile.write("  fields:" + '\n')
        yamlfile.write("    broadcaster: " + broadcaster + '\n')
        yamlfile.write("    slug: " + slugify(broadcaster) + '\n')
        yamlfile.write('\n')
