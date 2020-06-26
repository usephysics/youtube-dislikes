import requests
import re
import time
from bs4 import BeautifulSoup

# https://en.wikipedia.org/wiki/List_of_most-disliked_YouTube_videos

# goes through the page history and returns 1 URL for each month
def get_URLS():
    # initial URL to start
    URL = "https://en.wikipedia.org/w/index.php?title=List_of_most-disliked_YouTube_videos&action=history"
    URLs = []
    months = ["January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"]
    num_months = 49 # number of months in domain
    active_month = ""   # check used to only return 1 URL per month
    while len(URLs) < num_months:
        page = requests.get(URL).text
        soup = BeautifulSoup(page, "lxml")
        table = soup.find(id="pagehistory").findAll("li")
        # look at every date on page, except the first because it doesn't fit format
        for entry in table[1:]:
            if len(URLs) < num_months:
                date = entry.findAll("a")[2].text
                for month in months:
                    if month in date and month != active_month:
                        active_month = month
                        idx = date.index(month[0]) # to add year as well as month
                        URLs.append(("https://en.wikipedia.org" + entry.findAll("a")[2]["href"], date[idx:]))
        URL = "https://en.wikipedia.org" + soup.find("a", {"class":"mw-nextlink"})["href"]
        time.sleep(2) # wikipedia pls no ban
    return URLs

# this function visits a given URL and returns a list containing the top 10 most disliked videos
# with their title, uploader, and numbr of dislikes in millions.
def scrape_page(URL):
    page = requests.get(URL).text
    soup = BeautifulSoup(page, "lxml")
    table = soup.find("tbody").findAll("tr")
    entries = table[1:11] # rank 1 - 10
    videos = []

    for row in entries:
        title = re.findall(r'"([^"]*)"', row.findAll(["th", "td"])[1].text)[0]
        if title == "YouTube Spotlight": title: "YouTube" # name change mid way through
        uploader = row.findAll(["th", "td"])[2].text
        dislikes = row.findAll(["th", "td"])[3].text
        # earlier versions of the page used thousands of dislikes as their unit
        if float(dislikes) > 150: dislikes = str(float(dislikes) / 1000)
        videos.append([title, uploader, dislikes])
    return(videos)

data = []
URLs = get_URLS()
while(URLs):
    URL, month = URLs.pop()
    data.append([month, scrape_page(URL)])

file = open("data.py", "a")
file.write(str(data))
file.close()

# data[] --> Represents a month, ex: all data for June 2020
# data[][0] --> The month as a string, ex: "June 2020"
# data[][1] --> The top 10 for a given month, ex: List holding all info for top 10 most disliked videos in June 2020
# data[][1][x] --> The placement for the given month. ex: The xth most disliked video for June 2020
# data[][1][x][y] --> The data. 0 = Title, 1 = Uploader, 2 = Dislikes. ex: "YouTube Rewind 2018"