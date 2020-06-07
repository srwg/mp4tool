#!/usr/bin/env python

import os, sys

BAD = '/Users/ningma/ks/recode/'
DONE = BAD + 'cut/'
MISSING_STREAM = BAD + 'missing_stream/'
REVERSED_STREAM = BAD + 'reversed_stream/'
RESIZE = BAD + 'resize/'
CROP = BAD + 'crop/'
CHANGE_FPS = BAD + 'change_fps/'

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
  'time_base': '1/24000',
  'codec_tag': '0x6134706d',
  'channel_layout': 'stereo',
  'sample_rate': '24000'
}

def get_scale(w, h):
  w = int(w)
  h = int(h)
  if 1.222 < w * 1.0 / h < 1.444:
    return 'scale=480:360'
  if 1.666 < w * 1.0 / h < 1.889:
    return 'scale=640:360'
  if 2.222 < w * 1.0 /h  < 2.444:
    return 'scale=840:360'
  return None

def get_crop2(new_w, new_h, dw, dh, w, h):
  w2 = int(new_w)
  h2 = int(new_h)
  dw = int(dw)
  dh = int(dh)
  w = int(w)
  h = int(h)
  if w - w2 <= 4 and h - h2 <= 4: return None
  if w - w2 > 4:
    w2+= 4
    dw-= 2
    if dw < 0: dw = 0
  if h - h2 > 4:
    h2+=4
    dh-= 2
    if dh < 0: dh = 0
  return 'crop=' + str(w2) + ':' + str(h2) + ':' + str(dw) + ':' + str(dh)
  
def change_fps(f, v):
  if v['r_frame_rate'] == '25/1': return False
  #old_n, old_d =  v['avg_frame_rate'].split('/')
  #t_scale2 = 25.0 * int(old_d) / int(old_n)
  #if not 0.83 < t_scale2 < 1.15: return False
  old_rate_n, old_rate_d = v['r_frame_rate'].split('/')
  t_scale = 25.0 * int(old_rate_d) / int(old_rate_n)
  if not 0.83 < t_scale < 1.15: return False
  a_option = ' -af atempo=' + str(t_scale) + A_OPTION
  g = open('sh_' + f[:-3] + 'sh', 'w')
  g.write('rm -rf _video.h264 _audio.mp4\n')
  g.write('ffmpeg -i "' + f + '" -an -c:v copy _video.h264\n')
  g.write('ffmpeg -i "' + f + '" -vn ' + a_option + ' _audio.mp4\n')
  g.write('mp4box "' + CHANGE_FPS + f + '" -add _video.h264:fps=25 -add _audio.mp4\n')
  g.write('rm -rf _video.h264 _audio.mp4\n')
  g.close()
  print f + ' needs fps change.'
  return True
  
def check(f, CHECK_CROP=False):  
  g = f[:-3] + 'info'
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
  
  if len(streams) != 2:
    os.rename(f, MISSING_STREAM + f)
    os.rename(g, MISSING_STREAM + g)
    print f + ' is missing stream.'
    return
  
  v = streams[0]
  a = streams[1]
  if (v['codec_type'] == 'audio'):
    os.rename(f, REVERSED_STREAM + f)
    os.rename(g, REVERSED_STREAM + g)
    print f + ' HAS REVERSED streams seq'
    return

  if change_fps(f, v): return

  v_option = '-c:v copy '
  if v['width'] != v['coded_width'] or v['height'] != v['coded_height']:
    print 'coded size does not match size'
    v_option = V_OPTION
  else:
    for k in golden_v.keys():
      if v[k] != golden_v[k]:
        print f + ' ' + k + ': ' + v[k]
        v_option = V_OPTION
        break

  a_option = '-c:a copy '
  d = float(v['duration']) - float(a['duration'])
  t = float(v['duration'])
  if d * d > 1 and d * d / t / t >  0.00001:
    print f + ' needs resync.'
    speed_scale = float(a['duration']) / float(v['duration'])
    a_option = ' -af atempo=' + str(speed_scale) + A_OPTION
  else:
    for k in golden_a.keys():
      if a[k] != golden_a[k]:
        print f + ' ' + k + ': ' + a[k]
        a_option = A_OPTION
        break

  if CHECK_CROP:
    os.system('rm -rf _crop')
    os.system('ffmpeg -i "' + f + '" -t 1 -vf cropdetect=24:2:0 -f null - 2>&1 | awk \'/crop/{print $NF}\' | tail -1 > _crop')
    crop = open('_crop', 'r').readline().strip()
    w, h, dx, dy = crop.split('=')[1].split(':')
    scale = get_scale(w, h)
    if not scale:
      scale = 'scale=$1:360'
    new_w = int(w) * 360 / int(h)
    new_f = 'sh' + f[:-4] + '__' + v['width'] + '_' + v['height'] + '_' + w + '_' + h + '_' +  str(new_w) + '.sh'
    g = None
    if v['width'] != w or v['height'] != h:
      os.rename(f, CROP + f)
      g = open(CROP + new_f, 'w')
    else:
      g = open(new_f, 'w')
    crop2 = get_crop2(w, h, dx, dy, v['width'], v['height'])
    if crop2:
      crop = crop2
    g.write('# original size: ' + v['width'] + 'x' + v['height'] +'\n')
    g.write('crop="' + crop + '"\n')
    g.write('if [ "$#" -eq 2 ]; then\n')
    g.write('  ffmpeg -i "' + f + '" -vf $crop,' + scale + ',setsar=1/1 ' + V_OPTION + a_option + '"' + DONE + f + '"\n')
    g.write('else\n')
    g.write('  ffplay -i "' + f + '" -an -vf $crop,' + scale  + ',setsar=1/1\n')
    g.write('fi\n')
    g.close()
    print f + ' needs crop.'
    return
  
  # SAR, DAR
  w = v['width']
  h = v['height']
  if w + h not in ['840360', '640360', '480360'] or v['sample_aspect_ratio'] != '1:1':
    scale = get_scale(w, h)
    if scale:
      open('sh_' + f[:-3] + 'sh', 'w').write('ffmpeg -i "' + f + '" -vf ' + scale + ',setsar=1/1 ' + V_OPTION + a_option + '"' + DONE + f + '"\n')
      return
    os.rename(f, RESIZE + f)
    new_w = int(w) * 360 / int(h)
    new_f = RESIZE + 'sh_' + f[:-4] + '__' + str(new_w) + '.sh'
    g = open(new_f, 'w')
    g.write('if [ "$#" -eq 2 ]; then\n')
    g.write('  ffmpeg -i "' + f + '" -vf scale=$1:360,setsar=1/1 ' + V_OPTION + a_option + '"' + DONE + f + '"\n')
    g.write('else\n')
    g.write('  ffplay -i "' + f + '" -an -vf scale=$1:360,setsar=1/1\n')
    g.write('fi\n')
    g.close()
    print f + ' needs resize.'
    return

  if v_option == '-c:v copy ' and a_option == '-c:a copy ':
    return
  
  open('sh_' + f[:-3] + 'sh', 'w').write('ffmpeg -i "' + f + '" ' + v_option + a_option + '"' + DONE + f + '"\n')
   

if __name__ == '__main__':
  f = sys.argv[1]
  CHECK_CROP = False
  if len(sys.argv) > 2:
    CHECK_CROP = True
  check(f, CHECK_CROP)
