import urllib2
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import re
import sys

def lyricsMint(song, save):
    url = "http://www.lyricsmint.com/search?q="+"+".join(song.split())
    req = urllib2.Request(url=url)
    html = urllib2.urlopen(req)
    soup = BeautifulSoup(html)
    soup = soup.select('.blog-posts.hfeed .date-outer')

    lyric = None
    href = []
    for s in soup:
        temp = s.select('.post-title a')[0]
        for name in songName.split():
            if name.lower() in temp.text.lower():
                href.append((temp.text, temp['href']))
                break
    if href == []:
        for i in range(soup.__len__()):
            title = soup[i].select('.post-title a')[0]
            print i, title.text
        choice = input("Enter the choice")
        lyric = (soup[choice].select('.post-title a')[0].text, soup[choice].select('.post-title a')[0]['href'])
    elif href.__len__() == 1:
        lyric = href[0]
    else:
        for i in range(href.__len__()):
            print i, href[i][0]
        choice = input("Enter the choice")
        lyric = href[choice]
    file = open(save, 'w')
    file.write("")
    print lyric
    
    url = lyric[1]
    req = urllib2.Request(url=url)
    html = urllib2.urlopen(req)
    soup = BeautifulSoup(html)
    soup = soup.select('#lyric')
    print soup

sys.argv.pop(0)
saveTo = None
while sys.argv.__len__() != 0:
    options = sys.argv.pop(0)
    if options == '-o' or '--ouput':
        saveTo = sys.argv.pop(0)
songName = "Banjara"
lyricsMint(songName, saveTo)
