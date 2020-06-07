#!/usr/bin/env python

import os, sys, subprocess
from PIL import Image

BAD = '/Users/ningma/ks/work/'
MISSING_STREAM = BAD + 'missing_stream/'
REVERSED_STREAM = BAD + 'reversed_stream/'
CHANGE_FPS = BAD + 'duration/'
DONE = '/Users/ningma/ks/mp4/'

V_OPTION = ' -r 25 -video_track_timescale 25000 -pix_fmt yuv420p -c:v libx264 -profile:v high -level 3.1 -crf 20 -g 250 -keyint_min 5 -sc_threshold 80 -refs 2 '

A_OPTION = ' -ar 24000 -ac 1 -c:a libfdk_aac -profile:a aac_he -vbr 1 '

golden_v = {
  'profile': 'High',
  'codec_tag': '0x31637661',
  'has_b_frames': '2',
  'pix_fmt': 'yuv420p',
  'refs': '1',
  'level': '31',
  'chroma_location': 'left',
  'time_base': '1/25000',
  'r_frame_rate': '25/1'
}
  
golden_a = {
  'channels': '2',
  'profile': 'HE-AAC',
  #'time_base': '1/24000',
  'codec_tag': '0x6134706d',
  'channel_layout': 'stereo',
  'sample_rate': '24000'
}

def execute(f, g, dir):
  os.rename(f, dir + f)
  if dir != DONE:
    os.rename(g, dir + g)
  print f + ' moved to ' + dir
  return

def get_scale(w, h):
  w = int(w)
  h = int(h)
  wh = w * 1.0 / h
  if wh < 1.5:
    return 'scale=480:360'
  if wh < 2.0:
    return 'scale=640:360'
  else:
    return 'scale=840:360'

def assign(f):
  g = f[:-3] + 'info'
  streams = getMeta(f, g)
  verify(f, g, streams)

def getMeta(f, g):
  if not os.path.exists(g):
    os.system('ffprobe -v quiet -show_streams "' + f + '" > "' + g + '"')
  streams = []
  s = None
  for l in open(g).readlines():
    l = l.strip()
    if l == '[STREAM]':
      s = {}
    elif l == '[/STREAM]':
      streams.append(s)
    else:
      try:
        k,v = l.split('=')
        s[k] = v
      except: pass
  return streams
  
def verify(f, g, streams):
  if len(streams) != 2:
    execute(f, g, MISSING_STREAM)
    return
  
  v = streams[0]
  a = streams[1]
  if (v['codec_type'] == 'audio'):
    execute(f, g, REVERSED_STREAM)
    return

  if v['r_frame_rate'] != '25/1':
    #old_rate_n, old_rate_d =  v['avg_frame_rate'].split('/')
    old_rate_n, old_rate_d = v['r_frame_rate'].split('/')
    t_scale = 25.0 * int(old_rate_d) / int(old_rate_n)
    if 0.83 < t_scale < 1.15:
      a_option = ' -af atempo=' + str(t_scale) + A_OPTION
      os.system('rm -rf _video.h264 _audio.mp4')
      os.system('ffmpeg -i "%s" -an -c:v copy _video.h264' %f)
      os.system('ffmpeg -i "%s" -vn %s _audio.mp4' %(f, a_option))
      os.system('mv "%s" "fps_%s"' %(f, f))
      os.system('mp4box "%s" -add _video.h264:fps=25 -add _audio.mp4' %f)
      os.system('rm -rf _video.h264 _audio.mp4 "%sinfo"' %f[:-3])
      streams = getMeta(f, g)
      v = streams[0]
      a = streams[1]

  w = v['width']
  h = v['height']
  v_option = '-c:v copy '
  if w != v['coded_width'] and v['coded_width'] != '848' or v['coded_height'] != '368':
    v_option = V_OPTION
  else:
    for k in golden_v.keys():
      if v[k] != golden_v[k]:
        v_option = V_OPTION
        break

  a_option = '-c:a copy '
  vt = float(v['duration'])
  at = float(a['duration'])
  d = vt - at
  t_scale = at / vt
  if d * d > 0.64 and (t_scale < 0.985 or  1.02 < t_scale):
    if t_scale < 0.83 or t_scale > 1.15:
      execute(f, g, CHANGE_FPS)
      return
    a_option = ' -af atempo=' + str(t_scale) + A_OPTION
  else:
    for k in golden_a.keys():
      if a[k] != golden_a[k]:
        a_option = A_OPTION
        break

  vf = ''
  if os.path.exists(f[:-3] + 'meta'):
    vf = ' ' + open(f[:-3] + 'meta').readline().strip()
  elif w + h not in ['840360', '640360', '480360'] or v['sample_aspect_ratio'] != '1:1':
    vf = ' -vf ' + get_scale(w, h) + ',setsar=1/1'

  if vf != '':
    v_option = vf + V_OPTION
    
  if v_option == '-c:v copy ' and a_option == '-c:a copy ':
    execute(f, g, DONE)
    return

  open('run.sh', 'a').write('ffmpeg -i "%s" %s %s "%s%s"\n' %(f, v_option, a_option, DONE, f))
  return
   

if __name__ == '__main__':
  f = sys.argv[1]
  assign(f)
