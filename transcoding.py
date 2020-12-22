#!/usr/bin/env python

import sys
lines = open(sys.argv[1], 'r').readlines()

g = open(sys.argv[1], 'w')
for l in lines:
	g.write(l.decode('gb2312').encode('utf-8'))
g.close()
