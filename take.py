#!/usr/bin/env python

import glob, sys, os

N = int(sys.argv[1])

k = 0
for i in glob.glob('*.mp4'):
  os.rename(i, '/Users/ningma/ks/mp4/' + i)
  k += 1
  if k == N: break

