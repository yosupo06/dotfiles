#!/usr/bin/env python3

from subprocess import run, check_call
from pathlib import Path
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('source', help='source file')
args = parser.parse_args()

src = Path(args.source)
stem = src.stem
ext = src.suffix

# compile
if ext == '.cpp':
    cxxargs = ['g++']
    cxxargs.extend(['-std=c++14'])
    cxxargs.extend(['-Wall', '-Wextra', '-Wshadow', '-Wconversion'])
    cxxargs.extend(['-g'])
    cxxargs.extend(['-fsanitize=address,undefined', '-fno-sanitize-recover'])
    cxxargs.extend(['-fno-omit-frame-pointer'])
    cxxargs.extend(['-o', 'bin/{}'.format(stem)])  # output
    cxxargs.extend([src])
    check_call(cxxargs)
else:
    assert False, "unknown file type"

# test run
for infile in sorted(Path('tests').glob('*{}*.in'.format(stem))):
    print('##### Start {}'.format(infile), flush=True)
    t1 = datetime.now()
    r = run('./bin/{}'.format(stem),
            stdin=open(infile, 'r'),
            env={'UBSAN_OPTIONS': 'print_stacktrace=1'})
    t2 = datetime.now()
    print('##### return={} time={}ms'.format(
        str(r.returncode),
        str((t2-t1).microseconds//1000)))
