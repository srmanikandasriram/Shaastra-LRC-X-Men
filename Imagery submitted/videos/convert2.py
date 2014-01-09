#!/usr/bin

import sys
import subprocess

index = 1
f = open('values_videos.txt','r')
overlay_text = f.readline()
while overlay_text:
    print overlay_text
    filename1 = "LRC14_25_VD00" + str(index) + ".mp4"
    print filename1
    subprocess.call("ffmpeg -y -i video" + str(index) + ".raw -vf \"movie='image_overlay.png' [logo], [in]drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf:box=1:boxcolor=black@0.3:text='" + overlay_text + " Team_ID LC32 Cam_ID 2':fontsize=30:fontcolor=white:x=100:y=10,[logo] overlay=0:0,scale=1920:1080 [out]\" " + filename1,shell=True)
    index = index+1
    overlay_text = f.readline()
