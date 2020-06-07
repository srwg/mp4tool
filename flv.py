#!/usr/bin/env python

import os
import glob

def flv2mp4():
  os.system('rm -f *.jpg _tmp.*')
  for i in glob.glob('*.flv'):
    os.system('ffmpeg -i "' +  i + '" -vcodec copy -bsf:v h264_mp4toannexb _tmp.h264 -acodec copy _tmp.aac')
    os.system('MP4Box -add _tmp.h264 -add _tmp.aac "' + i[:-3] + 'mp4"')
    os.system('rm -f _tmp.*')

if __name__ == "__main__":
  flv2mp4()
