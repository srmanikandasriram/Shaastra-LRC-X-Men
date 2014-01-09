#!/usr/bin

import sys
import subprocess

filename = str(sys.argv[1])
overlay_text = sys.argv[2:]
text = ""
for t in overlay_text:
    text += str(t) + " "
    print t
filename1 = "LRC14_25_IM00" + filename[-5] + ".jpg"
subprocess.call("ffmpeg -y -i " + filename + " -vf \"movie='image_overlay.png' [logo], [in]drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf:box=1:boxcolor=black@0.3:text='" + text + " Team_ID LC32 Cam_ID 2':fontsize=30:fontcolor=white:x=100:y=10,[logo] overlay=0:0 [out]\" " + filename1,shell=True)
