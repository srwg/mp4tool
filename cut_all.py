#!/usr/bin/env python

AFTER_CUT = '/Users/ningma/ks/after_cut/'

def checkstatus(lastfn):
  return os.path.exists(lastfn)

def getsec(s):
  sec = s/1000
  ms = s%1000
  return '%d.%03d' %(sec, ms)

def gettime(l):
  b, e = l.strip().split()
  return ' -splitx ' + getsec(int(b)+10) + ':' + getsec(int(e)-10)

import os

def cut(fn):
  name = fn[:-4]
  index = 0
  fname  = AFTER_CUT + fn[:-3] + 'mp4'
  if os.path.exists(fname):
    os.rename(fname, AFTER_CUT + fn + '_bak')
  cmd2 = 'MP4Box "' + fname + '"'
  clean = 'rm'
  done = True
  hasLine = False
  for l in open('cut/' + name + '.cut').readlines():
    hasLine = True
    done = False
    cmd = 'MP4Box' + gettime(l) + ' "' + name + '.mp4" -out tmp' + str(index) + '.mp4'
    print cmd
    os.system(cmd)
    cmd2 += ' -cat tmp' + str(index) + '.mp4'
    clean += ' tmp' + str(index) + '.mp4'
    index += 1
    if index >= 15:
      os.system(cmd2)
      os.system(clean)
      index = 0
      cmd2 = 'MP4Box "' + fname + '"'
      clean = 'rm'
      done = True
  if not done:
    os.system(cmd2)
    os.system(clean)
  if not hasLine:
    os.rename(name + '.mp4', fname)
  else:
    os.rename(name + '.mp4', 'cut_' + name + '.mp4')
  #os.remove('cut/' + name + '.cut')

import glob, shutil
for c in glob.glob('cut/*.cut'):
  cut(c[4:])
