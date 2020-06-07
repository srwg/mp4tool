#!/usr/bin/env python

import glob
import sys, os
from mp4lib import crop

for i in glob.glob('*.mp4'):
  if not os.path.exists(i[:-3] + 'meta'):
    print i
    c = crop.Crop(i)
    c.start()
