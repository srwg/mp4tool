#!/usr/bin/env python

import glob
import os

VIDEO_ROOT='/Users/ningma/Desktop/y/'

for i in glob.glob('*'):
  if not i.endswith('meta'):
    mf = i[:-3] + 'meta'
    if os.path.exists(mf):
      l = open(mf).readline().strip()
      print 'ffmpeg -i ' + i + ' ' + l + ' -r 25 -video_track_timescale 25000 -pix_fmt yuv420p -c:v libx264 -profile:v high -level 3.1 -crf 20 -g 250 -keyint_min 1 -sc_threshold 90 -refs 2 -ar 24000 -ac 1 -c:a libfdk_aac -profile:a aac_he -vbr 1 ' + VIDEO_ROOT + i.split('.')[0] + '.mp4'
