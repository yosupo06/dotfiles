#!/usr/bin/env python3

from subprocess import run
from sys import argv, exit, stdout
from os.path import splitext, isfile
from datetime import datetime
import glob

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('exec', help='exec file')
parser.add_argument('-n', '--nobuild', action='store_true', help='no build')
args = parser.parse_args()

exec_file = args.exec

if not args.nobuild:
	run(['make', '-B', exec_file])

for in_file in sorted(glob.glob('tests/*{}*.in'.format(exec_file))):
	print('##### Start {}'.format(in_file))
	stdout.flush()
	t1 = datetime.now()
	r = run('./' + exec_file, stdin=open(in_file, 'r'))
	t2 = datetime.now()
	print('##### return={} time={}ms'.format(
        str(r.returncode),
        str((t2-t1).microseconds//1000)))
