# site_import.py imports site information from the ncb**.txt database
# Note that before we start, we need to open ncb18 and save it in utf-8 as it was created in Japanese Windows

import os, pandas, time, pycountry
from slugify import slugify
from functions import *
from geopy.geocoders import Nominatim

def is_null(latlon): # detect empty latlon fields
    latlon = str(latlon)
    if latlon == 'nan':
        return True
    else:
        return False

# Function for parsing the horrible latlon format used in the database
# We want, for example, Woofferton at 5219N00243W to be 52.19, -2.43
def get_latlon(latlon):
    latlon = str(latlon)
    length = len(latlon)
    lat = "0.00"
    lon = "0.00" # broken items go on Null Island for later fixing
    if length == 11:
        rawlat = latlon[0:5]
        rawlon = latlon[5:11]
        lat = rawlat[0:2] + '.' + rawlat[2:4]
        lon = rawlon[0:3] + '.' + rawlon[3:5]
        if rawlat[4] == 'N':
            lat = lat
        if rawlat[4] == 'S':
            lat = '-' + lat
        if rawlon[5] == 'E':
            lon = lon
        if rawlon[5] == 'W':
            lon = '-' + lon
    if length == 15:
        rawlat = latlon[0:7]
        rawlon = latlon[7:15]
        lat = rawlat[0:2] + '.' + rawlat[2:4]
        lon = rawlon[0:3] + '.' + rawlon[4:6]
        if rawlat[6] == 'N':
            lat = lat
        if rawlat[6] == 'S':
            lat = '-' + lat
        if rawlon[5] == 'E':
            lon = lon
        if rawlon[5] == 'W':
            lon = '-' + lon
    return lat, lon

def get_iso(latlon):
    geolocator = Nominatim(user_agent="shortwave2")
    c = geolocator.reverse(latlon)
    if str(c.raw)=="{'error': 'Unable to geocode'}":
        cc = 'xx'
    else:
        cc = c.raw['address']['country_code']
    iso = cc.upper()

    return iso

fh = open('sites.tmp', 'w')
with open('ncb18.txt') as skedfile:
    for line in skedfile:
        freq = (line[0:5].strip())
        mw = (is_freq_mw(freq))
        if mw == True:
            pass # ignore line if frequency is in the MW band
        if mw == False:
            sitename = (line[90:113]) # get site from file
            sitename = sitename.strip()
            if sitename == "?":
                sitename = "Unknown Site" # the questionmark breaks the import
            else:
                sitename = sitename
            latlon = (line[117:134])
            latlon = latlon.strip()
            site = sitename + '|' + latlon + '\n'
            if sitename == '': # we do not need transmissions with no site name, drop
                pass
            else:
                fh.write(site)
fh.close()

# We now have a file with all the site names from ncb18.txt but need to deduplicate
lines_seen = set() # create tuple
fh = open('sites.csv', 'w')
with open('sites.tmp') as sitesfile:
    for line in sitesfile:
        if line not in lines_seen: # not a duplicate
            fh.write(line)
            lines_seen.add(line)
fh.close()
os.remove('sites.tmp') # remove original file with dupes

# Let's import the sites and latlon into a pandas dataframe
fh = open('sites_fixed.csv', 'w')
df = pandas.read_csv('sites.csv', sep='|', names=['site', 'latlon'])
df = df.drop_duplicates(subset="site", keep="first")
for index, row in df.iterrows():
    latlon = row['latlon']
    if is_null(latlon) == True:
        lat = "0.00"
        lon = "0.00"
        fh.write(row['site'] + '|' + lat + '|' + lon + '\n')
    else:
        latlon = (get_latlon(latlon))
        lat = latlon[0]
        lon = latlon[1]
        fh.write(row['site'] + '|' + lat + '|' + lon + '\n')
fh.close()
os.remove('sites.csv')

# Now let's get a country from Nominatim for all the sites and write the yamlfile
df2 = pandas.read_csv('sites_fixed.csv', sep='|', names=['site', 'lat', 'lon'])
pk = 0
yamlfile = open('sites.yaml', 'w')
for index, row in df2.iterrows():
    pk = pk + 1
    lat = str(row['lat'])
    lon = str(row['lon'])
    if lon == "E15.13": # special snowflake case for Asmara
        lon = "15.13"
    else:
        lon = lon
    latlon = lat + ', ' + lon
    iso = get_iso(latlon)
    if iso=="XX":
        countryname = 'Unknown Country' # fix exception when point is in the sea
    else:
        country = pycountry.countries.get(alpha_2=iso)
        countryname = str(country.name)
    yamlfile.write("- model: shortwave.site" + '\n')
    yamlfile.write("  pk: " + str(pk) + '\n')
    yamlfile.write("  fields:" + '\n')
    yamlfile.write("    site: " + (row['site']) + '\n')
    yamlfile.write("    slug: " + slugify(row['site']) + '\n')
    yamlfile.write("    lat: " + lat + '\n')
    yamlfile.write("    lon: " + lon + '\n')
    yamlfile.write("    iso: " + iso + '\n')
    yamlfile.write("    countryslug: " + slugify(iso) + '\n')
    yamlfile.write("    countryname: " + countryname + '\n')
    yamlfile.write('\n')
    print("written site", pk, "-", row['site'], "in", countryname)
    time.sleep(1) # sleep for a second to avoid Nominatim rate limit
yamlfile.close()
os.remove('sites_fixed.csv')
