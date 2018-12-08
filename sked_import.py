import os, pandas, time, uuid
from slugify import slugify
from functions import *

def get_freq(freq):
    freq = freq.strip()
    freq = int(freq)
    return freq

def get_broadcaster(broadcaster):
    broadcaster = broadcaster.strip()
    if broadcaster == "?":
        broadcaster = "Unknown Broadcaster"
    elif broadcaster == "":
        broadcaster = "Unknown Broadcaster"
    return broadcaster

def get_times(time): # put times into Django friendly format
    timeon = (time[0:2] + ':' + time[2:4] + ':00')
    timeoff = (time[5:7] + ':' + time[7:9] + ':00')
    return timeon, timeoff

def get_days(days):
    # Days default to false
    sun = False
    mon = False
    tue = False
    wed = False
    thu = False
    fri = False
    sat = False
    if "1" in days:
        sun = True
    if "2" in days:
        mon = True
    if "3" in days:
        tue = True
    if "4" in days:
        wed = True
    if "5" in days:
        thu = True
    if "6" in days:
        fri = True
    if "7" in days:
        sat = True
    # Build the days string
    s = ''
    if mon == True:
        s = s + '    mon: true\n'
    else:
        s = s + '    mon: false\n'
    if tue == True:
        s = s + '    tue: true\n'
    else:
        s = s + '    tue: false\n'
    if wed == True:
        s = s + '    wed: true\n'
    else:
        s = s + '    wed: false\n'
    if thu == True:
        s = s + '    thu: true\n'
    else:
        s = s + '    thu: false\n'
    if fri == True:
        s = s + '    fri: true\n'
    else:
        s = s + '    fri: false\n'
    if sat == True:
        s = s + '    sat: true\n'
    else:
        s = s + '    sat: false\n'
    if sun == True:
        s = s + '    sun: true\n'
    else:
        s = s + '    sun: false\n'

    return s

def get_language(lang):
    lang = single_lang(lang)
    lang = lang.strip()
    if lang == "?":
        lang = "Unknown Language"
    elif lang == "":
        lang = "Unknown Language"
    return lang

def get_site(site):
    site = site.strip()
    if site == "?":
        site = "Unknown Site"
    elif site == "":
        site = "Unknown Site"
    else:
        site = site
    return site

def get_power(power):
    power = power.strip()
    if power == '':
        power = 1
    else:
        power = float(power)
    return power

def get_azimuth(azimuth):
    azimuth = azimuth.strip()
    if azimuth == 'ND':
        azimuth = 0
    if azimuth == '':
        azimuth = 0
    else:
        azimuth = int(azimuth)
    return azimuth

# Let's pull in the variables
pk = 0
yamlfile = open('sked.yaml', 'w')
with open('ncb18.txt') as skedfile:
    for line in skedfile:
        seed = line # for UUID generation
        freq = (line[0:5].strip())
        mw = (is_freq_mw(freq))
        if mw == True:
            pass # ignore line if frequency is in the MW band
        if mw == False:
            freq = get_freq(line[0:5])
            broadcaster = get_broadcaster(line[6:37])
            timeon = get_times(line[38:47])[0]
            timeoff = get_times(line[38:47])[1]
            days = get_days(line[48:55])
            lang = get_language(line[56:82]) # extract name of language
            site = get_site(line[90:113])
            power = get_power(line[82:85])
            azimuth = get_azimuth(line[86:89])
            #print(freq, broadcaster, timeon, timeoff, lang, site, power, azimuth)
            #fh.write(lang + '\n') # write to file with new line at end
            pk = pk + 1
            print("- model: shortwave.station")
            print("  pk:", str(pk))
            print("  fields:")
            print("    freq:", freq)
            print("    timeon:", "'" + timeon + "'")
            if timeoff == "24:00:00":
                print("    timeoff: '23:59:00'")
            elif timeoff == "00:00:00":
                print("    timeoff: '23:59:00'")
            else:
                print("    timeoff:", "'" + timeoff + "'")
            print(days)
            print("    broadcaster:")
            print("      -", slugify(broadcaster))
            print("    site:")
            print("      -", slugify(site))
            print("    lang:")
            print("      -", slugify(lang))
            print("    power:", power)
            print("    azimuth:", azimuth)
            print("    uuid:", uuid.uuid5(uuid.NAMESPACE_DNS, seed))
            print("")
#fh.close()
