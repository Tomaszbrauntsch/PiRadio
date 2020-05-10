#antenna work: https://www.youtube.com/watch?v=F0N0fNxvWl0
#antenna work: https://www.limontec.com/2018/10/hijacking-radio-fm-raspberry-pi.html
#90.1 FM potentially?
#backend
from flask import Flask, request, render_template, url_for

#requests and html work
import requests
from lxml import html

#youtube to mp3 download
import youtube_dl

#Setup for radio work
import os
import sys
sys.path.append("./PiFmRds/src")
import PiFm as PiFm

app = Flask(__name__)
#insert queue system for song requests besides one
queueNum = 0
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
            }],
            'outtmpl': 'queue' + str(queueNum) + '.%(etx)s',
            'quiet': False
        }
#insert radio work

@app.route('/')
def index():
    #insert radio work
    return render_template('index.html')

@app.route('/names')
def names():
    return 'names' + '1'

@app.route('/songrequest', methods=['POST'])
def get_data():
    #"https://www.youtube.com/results?search_query=the+nights+avicii"
    yturl = "https://www.youtube.com/results?search_query="
    songName = request.form['songname']
    songName = songName.split()
    #loops and appends to url
    for x in range(len(songName)):
        yturl = yturl + songName[x] + "+"
    yturl = yturl + "audio"
    #Looking for audio gives better results 
    #Make request to the yturl -> grabs content -> looks for anchor tag 
    #and with href, loops and tries to find the first video link
    yturlRequest = requests.get(yturl)
    ytPage = html.fromstring(yturlRequest.content)
    ytLinks = ytPage.xpath('//a/@href')
    xCount = 0
    while (ytLinks[xCount][0:6] != "/watch"):
        xCount += 1
    #creates the videolink
    ytID = ytLinks[xCount][9:]
    ytVideo = "https://www.youtube.com" + ytLinks[xCount]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([ytVideo])
    #sends song to radio station
    PiFm.play_freq("87.5", "queue0.wav")
    return "Video was processed and is being sent to station!"
