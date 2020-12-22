#!/usr/bin/env python
import glob, os, shutil

OUT_PATH = './'

def readtask(fn):
  attr = {}
  for l in open(fn).readlines():
    if len(l) < 1: continue
    if l[0] == '#': continue
    tokens = l.strip().split('=')
    if len(tokens) != 2: continue
    attr[tokens[0]] = tokens[1]
  return attr

def getname(name):
  i = 0
  oname = ''
  while i < len(name):
    if i+6 <= len(name) and name[i:i+2] == '\\u':
      oname += unichr(int('0x' + name[i+2:i+6], 16))
      i += 6
    else:
      oname += name[i]
      i += 1
  oname = oname.encode('utf-8')
  tokens = oname.split()
  if len(tokens) == 2 and len(tokens[1]) >=7:
    try:
      no = int(tokens[1][3:-3])
      if not os.path.exists(OUT_PATH + tokens[0]):
        os.mkdir(OUT_PATH + tokesn[0])
      oname = '%s/%02d' %(tokens[0], no)
    except: pass
  return oname

def checkstatus(lastfn):
  return os.path.exists(lastfn)

for task in glob.glob('*.task'):
  attr = readtask(task)
  suffix = '.' + attr['fileType']
  path = task[:-5] + '/'
  num = int(attr['numOfChapters'])
  lastfn = path + 'chapter' + str(num) + suffix
  if not checkstatus(lastfn):
    continue
  name = getname(attr['videoName'])
  print name
  if num == 1:
    os.rename(path + 'chapter1.mp4', OUT_PATH + name + suffix)
    shutil.rmtree(path)
  else:
    os.rename(path, OUT_PATH + name)
  os.remove(task)
  print '   done.'
