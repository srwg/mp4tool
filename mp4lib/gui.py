#!/usr/bin/env python

import os, Tkinter
from PIL import Image, ImageTk

class Gui:

  def onExit(self, event):
    self.root.quit()

  def onKey(self, event):
    if event.char == 't':
      self.d = 1
      self.dd = 2
      return True
    if event.char == 'b':
      self.d = 3
      self.dd = -2
      return True
    if event.char == 'l':
      self.d = 0
      self.dd = 2
      return True
    if event.char == 'r':
      self.d = 2
      self.dd = -2
      return True
    if event.char == '=':
      self.crop[self.d] += self.dd
      self.showCrop()
      return True
    if event.char == '-':
      self.crop[self.d] -= self.dd
      self.showCrop()
      return True
    self.callback(event)
    return True

  def onMouse(self, event):
    return True

  def __init__(self, w, h, callback):
    self.callback = callback
    self.root = Tkinter.Tk()
    self.wh = w, h
    self.resizeWindow(w, h)
    self.root.bind('<Escape>', self.onExit)
    self.root.bind('<Key>', self.onKey)
    self.cvs = Tkinter.Canvas(self.root, width=w, height=h)
    #self.cvs.bind('<ButtonRelease-1>', self.onMouse)
    #self.cvs.bind('<ButtonRelease-2>', self.onMouse)
    self.view = self.cvs.create_image([0,0], anchor=Tkinter.NW)
    self.crop = [0, 0, w, h]
    self.d = 0
    self.dd = 2
    self.crop1 = self.cvs.create_rectangle((0,0,w,-1), fill='#f0d0d0', width=0)
    self.crop2 = self.cvs.create_rectangle((w,0,w,h), fill='#f0d0d0', width=0)
    self.crop3 = self.cvs.create_rectangle((0,h,w,h), fill='#f0d0d0', width=0)
    self.crop4 = self.cvs.create_rectangle((0,0,-1,h), fill='#f0d0d0', width=0)
    self.cvs.pack(fill='both', expand=True)

  def resizeWindow(self, w, h):
    self.wh = w, h
    self.root.geometry('%dx%d' %(w + 2,h + 2))

  def showCrop(self):
    x1, y1, x2, y2 = self.crop
    w, h = self.wh
    self.cvs.coords(self.crop1, (0, 0, w, y1))
    self.cvs.coords(self.crop2, (x2, 0, w, h))
    self.cvs.coords(self.crop3, (0, y2, w, h))
    self.cvs.coords(self.crop4, (0, 0, x1-1, h))

  def showImage(self, image):
    w, h = self.wh
    self.image = ImageTk.PhotoImage(image)
    self.cvs.itemconfigure(self.view, image = self.image)
    self.showCrop()

  def getCrop(self):
    return self.crop
    x1, y1, x2, y2 = self.crop
    return '"crop=%d:%d:%d:%d"' %(x2-x1, y2-y1, x1, y1)

  def clearCrop(self):
    w, h = self.wh
    self.crop = [0, 0, w, h]
    self.showCrop()

  def start(self):
    self.root.mainloop()    
    
