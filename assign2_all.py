#!/usr/bin/env python

import glob
import sys
from mp4lib import assign2

for i in glob.glob('*.mp4'):
  if len(sys.argv) > 1:
    assign2.assign(i, True)
  else:
    assign2.assign(i)

for i in glob.glob('*.avi'):
  if len(sys.argv) > 1:
    assign2.assign(i, True)
  else:
    assign2.assign(i)

for i in glob.glob('*.rmvb'):
  if len(sys.argv) > 1:
    assign2.assign(i, True)
  else:
    assign2.assign(i)
