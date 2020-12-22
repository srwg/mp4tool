#!/usr/bin/env python

import os, sys, subprocess
import gui
from PIL import Image

class Crop:

  def __init__(self, f):
    self.f = f
    self.t = 0
    self.scale = ''
    image = self.getSnapshot()
    w, h = image.size
    self.wh = (w, h)
    self.g = gui.Gui(w, h, self.onKey)
    self.g.showImage(image)

  def start(self):
    self.g.start()

  def onKey(self, event):
    if event.char == 'n':
      self.t += 4
      self.g.showImage(self.getSnapshot())
      return True
    if event.char == 'N':
      self.t += 20
      self.g.showImage(self.getSnapshot())
      return True
    if event.char == 'p':
      self.t -= 4
      if self.t < 0: self.t = 0
      self.g.showImage(self.getSnapshot())
      return True
    if event.char == 'v':
      crop = self.computeCrop()
      self.getSnapshot(crop)
      os.system('open _tmp.jpg')
      return True
    if event.char == 's':
      self.save()
      return True
    if event.char == '8':
      self.scale = 'scale=840:360' 
      return True
    if event.char == '6':
      self.scale = 'scale=640:360' 
      return True
    if event.char == '4':
      self.scale = 'scale=480:360' 
      return True
    return False

  def save(self):
    crop = self.computeCrop()
    if crop != '':
      print '  ' + crop
      open(self.f[:-3] + 'meta', 'w').write(crop + ',setsar=1/1\n')

  def computeCrop(self):
    crop = ''
    x1, y1, x2, y2 = self.g.getCrop()
    w = x2 - x1
    h = y2 - y1
    if self.wh != (w, h):
      crop = 'crop=%d:%d:%d:%d' %(w, h, x1, y1)
    if (w,h) in [(480,360), (640,360), (840,360)] and not self.scale:
      self.scale = ''
    elif self.scale == '':
      wh = w * 1.0 / h
      if wh < 1.5:
        self.scale = 'scale=480:360' 
      elif wh < 2.0:
        self.scale = 'scale=640:360'
      else:
        self.scale = 'scale=840:360'
    if crop == '':
      if self.scale == '':
        return ''
      else:
        return '-vf ' + self.scale
    else:
      if self.scale == '':
        return '-vf ' + crop
      else:
        return '-vf ' + crop + ',' + self.scale

  def getSnapshot(self, crop=''):
    m = self.t / 60
    s = self.t % 60
    os.system('rm -rf _tmp.jpg')
    os.system('ffmpeg -v quiet -i "%s" %s -ss 00:%02d:%02d -vframes 1 _tmp.jpg' %(self.f, crop, m, s))
    return Image.open('_tmp.jpg')

if __name__ == '__main__':
  f = sys.argv[1]
  c = Crop(f)
  c.start()
