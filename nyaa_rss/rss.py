import feedparser
import webbrowser
import json
import datetime, time
import os

#Hashes to dont save thing multiple times
hashes = []

#Load congif
with open('config.json', 'r') as f:
    config = json.load(f)
#Set config vars
isprinttoconsole = config["PrintToConsole?"]
iswritetofile = config["WriteToFile?"]
categorys = config["categorys"]
checktrusted = config["checktrusted"]
savetopath = config["savetopath"] 
refreshrate = config["refreshrate"]


#Check with config
def check(a, b, c):
    #a = kategória
    #b = istrusted
    #c = hash
    if checktrusted == 1 and b == "Yes":
        if categorys[a] == 1 and not (c in hashes):
            hashes.append(c)
            return True
    return False

#Print to console
def printtoconsole():
    print(nyaa["nyaa_title"], "\n")
    print(nyaa["nyaa_torrent_link"])
    print(nyaa["nyaa_link"])
    print("S: ", nyaa["nyaa_seeders"] , "/ L: ", nyaa["nyaa_leechers"] , "/ D: ", nyaa["nyaa_downloads"])
    print("Size: ", nyaa["nyaa_size"])
    print("Trusted: ", nyaa["nyaa_istrusted"])
    print("\n\n")

#Write to file
def writetofile(d):
    with open(savetopath, "a") as f:
        f.write("\n<<<<<<<<" + d.strftime("%x") + ">  :  <" + d.strftime("%X") + ">>>>>>>>\n" )
        f.write(nyaa["nyaa_title"] + "\n")
        f.write(nyaa["nyaa_torrent_link"] + "\n")
        f.write(nyaa["nyaa_link"] + "\n")
        f.write("Seeders: " + nyaa["nyaa_seeders"] + "/ Leechers: " + nyaa["nyaa_leechers"] + "/ Total Downloads: " + nyaa["nyaa_downloads"] + "\n")
        f.write("Size: " + nyaa["nyaa_size"] + "\n")
        f.write("Trusted: " + nyaa["nyaa_istrusted"])
        f.write("\n\n")

#Write to JSOn file for web
def writetojson(title,tlink,link,size,ist):
    ## Need to make path a variable
    with open('data.json', 'r') as f:
        data = json.load(f)
    #Parse the JSON to see how many entry are there
    entrynum = 0

    #MAKE THAT ERROR GO AWAY
    for x in data:
        entrynum += 1

    #JSON format
    currentry = {
        "title" : title,
        "details" : {
            "t_link" : tlink,
            "link" : link,
            "size" : size,
            "IsTrusted" : ist
        }
    }

    data[entrynum+1] = currentry
    ## Need to make path a variable
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
            
while True:

    ## Need to make Sukabei possible :)
    #Parse the RSS
    feed = feedparser.parse("https://nyaa.si/?page=rss")
    feed_entries = feed.entries

    #Parse the XML
    for entry in feed.entries:
        
        nyaa = {}
        
        today = datetime.datetime.now()

        #Title
        nyaa["nyaa_title"] = entry.title
        nyaa["nyaa_title_detail"] = entry.title_detail
        #nyaa_title = entry.title
        #nyaa_title_detail = entry.title_detail
        #Links
        nyaa["nyaa_torrent_link"] = entry.link
        nyaa["nyaa_link"]  = entry.guid
        #nyaa_torrent_link = entry.link
        #nyaa_site_link = entry.guid

        #S/L/D
        nyaa["nyaa_seeders"] = entry.nyaa_seeders
        nyaa["nyaa_leechers"] = entry.nyaa_leechers
        nyaa["nyaa_downloads"] = entry.nyaa_downloads
        #nyaa_seeders = entry.nyaa_seeders
        #nyaa_leechers = entry.nyaa_leechers
        #nyaa_downloads = entry.nyaa_downloads
        

        nyaa["nyaa_size"] = entry.nyaa_size
        nyaa["nyaa_istrusted"] = entry.nyaa_trusted
        nyaa["nyaa_category"] = entry.nyaa_category
        nyaa["nyaa_infoHash"] = entry.nyaa_infohash
        # nyaa_size = entry.nyaa_size
        # nyaa_istrusted = entry.nyaa_trusted
        # nyaa_category = entry.nyaa_category

        #Print
        if  check(nyaa["nyaa_category"],nyaa["nyaa_istrusted"],nyaa["nyaa_infoHash"]):
            
            writetojson(nyaa["nyaa_title"],nyaa["nyaa_torrent_link"],nyaa["nyaa_link"],nyaa["nyaa_size"],nyaa["nyaa_istrusted"])
            if iswritetofile : writetofile(today)
            if isprinttoconsole : printtoconsole()
    time.sleep(refreshrate)