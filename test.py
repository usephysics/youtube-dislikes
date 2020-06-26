import requests
import re
import time
from bs4 import BeautifulSoup

# https://en.wikipedia.org/wiki/List_of_most-disliked_YouTube_videosp

# goes through the page history and returns 1 URL for each month
def get_URLS():
    # initial URL to start
    URL = "https://en.wikipedia.org/w/index.php?title=List_of_most-disliked_YouTube_videos&action=history"
    URLs = []
    months = ["January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"]
    active_month = ""
    while len(URLs) < 5:
        page = requests.get(URL).text
        soup = BeautifulSoup(page, "lxml")
        table = soup.find(id="pagehistory").findAll("li")
        for entry in table[1:]:
            if len(URLs) < 5:
                date = entry.findAll("a")[2].text
                for month in months:
                    if month in date and month != active_month:
                        active_month = month
                        URLs.append(("https://en.wikipedia.org" + entry.findAll("a")[2]["href"], month))
        URL = "https://en.wikipedia.org" + soup.find("a", {"class":"mw-nextlink"})["href"]
    return URLs

# this function visits a given URL and returns a list containing the top 10 most disliked videos
# with their title, uploader, and numbr of dislikes in millions.
def scrape_page(URL):
    page = requests.get(URL).text
    soup = BeautifulSoup(page, "lxml")
    table = soup.find("tbody").findAll("tr")
    entries = table[1:11]
    videos = []

    for row in entries:
        title = re.findall(r'"([^"]*)"', row.findAll()[1].text)[0]
        uploader = row.findAll(["th", "td"])[2].text
        dislikes = row.findAll(["th", "td"])[3].text
        if float(dislikes) > 150: dislikes = float(dislikes) / 1000
        videos.append([title, uploader, dislikes])
    return(videos)