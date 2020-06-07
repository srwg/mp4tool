#!/usr/bin/env python

IN_DIR = r'/Users/tt/mp4/kuaishou/'
OUT_DIR  = r'/Users/tt/mp4/'

import glob, os, shutil

def join_dir(d):
    os.chdir(OUT_DIR + d)
    flist = []
    index = 1
    cmd = '/Users/tt/bin/MP4Box ' + OUT_DIR + d + '.mp4 '
    while os.path.exists('chapter' + str(index) + '.mp4'):
        cmd += ' -cat ' + 'chapter' + str(index) + '.mp4'
        index += 1
    if index > 1: 
        os.system(cmd)
        if os.path.exists(OUT_DIR + d + '.mp4'): return True
    return False

task_files = glob.glob(IN_DIR + '*.task')
print task_files

for t_file in task_files:

    print 'processing ' + t_file

    # read task
    task = {} 
    for line in open(t_file, 'rb').readlines():
        if line[0] == '#': continue
        items = line.strip().split('=')
        if len(items) == 2:
            task[items[0]] = items[1]

    try:
        # we do not know how to process other type of files yet...
        suffix  = '.' + task['fileType']

        # check if the task is completed
        in_dir = os.path.join(IN_DIR, task['mediaFileDir'].split('/')[-2])
        n_chapters = int(task['numOfChapters'])
        if n_chapters<1 or not os.path.exists(in_dir + '/chapter' + str(n_chapters) + suffix): 
            print '   not finished yet.'
            continue

        # get the name
        dname = ''
        name = ''
        for word in task['videoName'].split('\\u'):
            if len(word)<4: continue
            try:
                name += unichr(int(word[:4],16)).encode('utf-8')
            except:
                name += 'X'
            if len(word)>4:
                if len(word)==5 and '0' <= word[4] <= '9':
                    name += '0' + word[4] 
                else:
                    name += word[4:]
        if len(name)>6 and '0' <= name[-5] <= '9' and '0' <= name[-4] <= '9':
            dname = name[:-9]
            name = name[-5:-3]
        print '   name: ' + dname + '/' + name

        # process
        if dname!='': 
            if not os.path.exists(OUT_DIR + dname):
                os.mkdir(OUT_DIR + dname)
            name = dname + '/' + name
        if n_chapters == 1: 
            shutil.move(in_dir + '/chapter1' + suffix,  OUT_DIR + name + suffix)
        else:
            shutil.move(in_dir, OUT_DIR + name)
            if join_dir(name):
                shutil.rmtree(OUT_DIR + name)
	
        shutil.rmtree(in_dir)
        os.remove(t_file)
        print '   Successful'
    except:
        print '   Fails'
