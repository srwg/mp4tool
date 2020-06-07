#!/usr/bin/env python
import os, glob
import flv

for i in glob.glob('*'):
  try: os.chdir(i)
  except: continue
  try: flv.flv2mp4()
  except: print 'error: ' + i
  os.chdir('..')
