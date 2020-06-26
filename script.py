import requests
import re
from bs4 import BeautifulSoup

# https://en.wikipedia.org/wiki/List_of_most-disliked_YouTube_videos

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

print(scrape_page("https://en.wikipedia.org/wiki/List_of_most-disliked_YouTube_videos"))