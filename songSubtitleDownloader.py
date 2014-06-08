import urllib2
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import re
import sys
from mutagen.mp3 import MP3
from os import walk

def Help():
    h = '\n'
    h += 'usage: python songSubtitleDownloader.py [option] ... [-i file | -d directory] ...\n'
    h += '-i \t: input file source\n'
    h += '-d \t: input folder source\n'
    h += '-h \t: help'
    return h

def getCmd():
    #Cheking for help cmd
    for i in sys.argv:
        if i in ('-h', '--help'):
            return '-h', None

    # Return first most instruction, source
    temp = sys.argv.pop(0)
    if temp in ('-i', '--input', '-d', '--directory'):
        instruction = temp
    else:
        sys.exit("Command Error:" + Help())

    temp = sys.argv.pop(0)
    if not temp.startswith('-'):
        return instruction, temp
    else:
        sys.exit("Command Error:" + Help())

def lyricsMint(song, album, save):
    print song, "Searching..."
    # Searching Song
    url = "http://www.lyricsmint.com/search?q="+"+".join(song.split())
    req = urllib2.Request(url=url)
    html = urllib2.urlopen(req)
    soup = BeautifulSoup(html)
    soup = soup.select('.blog-posts.hfeed .date-outer')

    #No Lyrics
    if soup.__len__() == 0:
        print "No Lyrics found"
        return
    lyric = None
    href = []
    song = ''.join(ch for ch in song if ch.isalnum() or ch.isspace())
    album = ''.join(ch for ch in album if ch.isalnum() or ch.isspace())

    #Searching require lyric
    for s in soup:
        temp = s.select('.post-title a')[0]
        for name in song.split():
            if name.lower() in temp.text.lower():
                href.append((temp.text, temp['href']))
                break
    
    if href.__len__() == 1:
        lyric = href[0]
    else:
        if href.__len__() == 0:
            for i in range(soup.__len__()):
                title = soup[i].select('.post-title a')[0]
                href.append((title.text, title['href']))
                #print i, title.text
            #choice = input("Enter the choice: ")
            #lyric = (soup[choice].select('.post-title a')[0].text, soup[choice].select('.post-title a')[0]['href'])
        else:
            pass

        temp = []
        for i in range(href.__len__()):
            for name in album.split():
                if name.lower() in href[i][0].lower():
                    temp.append(href[i])
                    break
        if temp.__len__() == 1:
            lyric = temp[0]
        else:
            for i in range(temp.__len__()):
                print i, temp[i][0]
            choice = input("Enter the choice: ")
            lyric = temp[choice]
    
    url = lyric[1]
    req = urllib2.Request(url=url)
    html = urllib2.urlopen(req)
    soup = BeautifulSoup(html)
    soup = soup.select('#lyric')
    file = open(save, 'w')
    file.write(soup[0].select('p')[0].text)
    file.close()
    print 'Downloaded!'
    
sys.argv.pop(0)

while sys.argv.__len__() != 0:
    instruction, source = getCmd()
    source = source.replace('\\', '')

    # For one file
    if instruction in ('-i', '--input'):
        mut = MP3(source)
        songName = mut['TIT2'].text[0]
        albumName = mut['TALB'].text[0]
        saveAs = source.rsplit('.', 1)[0] + '.srt'
        lyricsMint(songName, albumName, saveAs)
    
    # For a folder
    if instruction in ('-d', '--directory'):
        for (dirPath, dirName, fileName) in walk(source):
            for f in fileName:
                if not f.rsplit('.', 1)[-1] == 'mp3':
                    continue
                mut = MP3(dirPath+f)
                songName = mut['TIT2'].text[0]
                albumName = mut['TALB'].text[0]
                saveAs = (dirPath+f).rsplit('.', 1)[0] + '.srt'
                lyricsMint(songName, albumName, saveAs)
                print "Done"
