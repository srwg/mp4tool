#!/usr/bin/env python

import glob, os

for d in glob.glob('*'):
  os.chdir(d)
  name = open('info','r').readline().split(',')[1].split(':')[1][1:-1]
  chapter = 1
  out = open(name + '.kux', 'wb')
  while True:
    fn = str(chapter)
    if os.path.exists(fn):
      out.write(open(fn,'rb').read())
    else:
      break
    chapter += 1
  out.close()

  os.system('ffmpeg -i "%s.kux" -vcodec copy -acodec copy "../%s.mp4"' %(name,name))
  os.chdir('..')
