#!/usr/bin/env python

import os, glob
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

def get_creation_time(exif_data):
  mtime = "?"
  if 306 in exif_data and exif_data[306] < mtime:
    mtime = exif_data[306]
  if 36867 in exif_data and exif_data[36867] < mtime:
    mtime = exif_data[36867]
  if 36868 in exif_data and exif_data[36868] < mtime:
    mtime = exif_data[36868]
  return mtime.replace(':','').replace(' ', '_')

for f in glob.glob('*.jpg'):
  img = Image.open(f)
  try:
    mtime = 'done/IMG_' + get_creation_time(img._getexif()) + '.jpg'
    os.rename(f, mtime)
  except:
    pass  

