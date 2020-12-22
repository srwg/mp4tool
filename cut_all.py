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
  if not os.path.exists(name + '.mp4'):
    return
  index = 0
  fname  = AFTER_CUT + fn[:-3] + 'mp4'
  if os.path.exists(fname):
    os.rename(fname, AFTER_CUT + fn + '_bak')
  fl = open('_list', 'w')
  clean = 'rm _list'
  hasLine = False
  for l in open('cut/' + name + '.cut').readlines():
    hasLine = True
    cmd = 'MP4Box' + gettime(l) + ' "' + name + '.mp4" -out _tmp' + str(index) + '.mp4'
    print cmd
    os.system(cmd)
    fl.write('file _tmp' + str(index) + '.mp4\n')
    clean += ' _tmp' + str(index) + '.mp4'
    index += 1
  fl.close()
  if not hasLine:
    os.rename(name + '.mp4', fname)
  else:
    cmd = 'ffmpeg -f concat -safe 0 -i _list -c copy "' + fname + '"'
    print cmd
    os.system(cmd)
    os.rename(name + '.mp4', 'cut_' + name + '.mp4')
    os.system(clean)
  os.remove('cut/' + name + '.cut')

import glob, shutil
for c in glob.glob('cut/*.cut'):
  cut(c[4:])
