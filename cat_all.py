#!/usr/bin/env python

import os

def cut(name, suffix):
  q1 = []
  q2 = []
  index = 0
  fn = name + '/chapter%d.%s' %(index, suffix)
  if os.path.exists(fn):
    q1.append(fn)
  index += 1
  fn = name + '/chapter%d.%s' %(index, suffix)
  while os.path.exists(fn):
    q1.append(fn)
    index += 1
    fn = name + '/chapter%d.%s' %(index, suffix)

  if not q1: return
  prefix = '_'
  cmd = ''
  while len(q1) > 1:
    j = 0
    for i in xrange(len(q1)):
      if i%15 == 0:
        if cmd:
          os.system(cmd)
          q2.append(fn)
        j += 1
        fn = prefix + str(j) + '.mp4'
        cmd = 'MP4Box ' + fn
      cmd += ' -cat ' + q1[i]
    os.system(cmd)
    q2.append(fn)
    q1 = q2
    q2 = []
    prefix += '_'
    cmd = ''

  try:
    os.rename(q1[0], name + '.mp4')
    os.system('rm -rf ' + name)
  except:
    pass

  os.system('rm -rf _*.mp4')

import glob
for i in glob.glob('*'):
  try:
    cut(i, 'mp4')
    cut(i, 'ts')
  except: pass
