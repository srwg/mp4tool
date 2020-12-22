#!/usr/bin/env python

import glob, sys, os

N = int(sys.argv[1])

after = []
for i in glob.glob('/Users/ningma/ks/after_cut/*/*.mp4'):
  after.append(i)

L = ''
k = 0
for i in glob.glob('*.mp4'):
  for j in after:
    if j.find(i) > 0:
      print i, j
      L += i + ' '
  os.rename(i, '/Users/ningma/ks/mp4/' + i)
  k += 1
  if k == N: break

print L
