#!/usr/bin/env python

import glob
import sys
from mp4lib import assign

for i in glob.glob('*.mp4'):
  if len(sys.argv) > 1:
    assign.assign(i, True)
  else:
    assign.assign(i)

