#!/usr/bin/env python3

import os
import argparse
import shutil
import toml
import onlinejudge
from pathlib import Path
from subprocess import check_call, run
from sys import exit
from os import getenv
from logging import Logger, basicConfig, getLogger

logger = getLogger(__name__)  # type: Logger


algbase = Path(os.environ['HOME']) / 'Programs' / 'Algorithm'

def build(src: Path):
    logger.info('Build {}'.format(src))
    cxxargs = [os.getenv('CXX', 'g++')]
    cxxargs.extend(['-std=c++17'])
    cxxargs.extend(['-Wall', '-Wextra', '-Wshadow',
                    '-Wconversion', '-Wno-unknown-pragmas'])
    cxxargs.extend(['-I{}'.format(str(algbase / 'src'))])
    cxxargs.extend(['-DLOCAL'])

    cxxargs.extend(['-g'])
    cxxargs.extend(['-fsanitize=address,undefined', '-fno-sanitize-recover'])
    cxxargs.extend(['-fno-omit-frame-pointer'])
    cxxargs.extend(['-o', src.stem])
    cxxargs.extend([src.name])

    check_call(cxxargs, cwd=src.parent)
    logger.info('Build Finished')


def ensure(msg):
    while True:
        s = input('{} OK? [y/N]:'.format(msg))
        if s in ['y', 'Y', 'yes', 'Yes']:
            break
        if s in ['n', 'N', 'no', 'No']:
            exit(0)


def command_init(args):
    if args.site not in ['atcoder', 'codeforces', 'opencup']:
        raise Exception()

    offline = args.site in ['opencup']
    if args.site == 'atcoder':
        if any([s.isupper() for s in args.problems]):
            ensure('Try to make uppercase problem {}'.format(args.problems))
    elif args.site == 'codeforces':
        if any([s.islower() for s in args.problems]):
            ensure('Try to make lowercase problem')

    base = Path(args.site + "-" + args.contest)
    base.mkdir()

    src = Path.home() / Path("Programs/Algorithm/src/base.cpp")

    for prob in args.problems:
        pdir = base / prob
        pdir.mkdir()
        shutil.copy(str(src), pdir / "main.cpp")
        if offline:
            cdir = pdir / 'test'
            cdir.mkdir()

    # make info.toml
    info = dict()
    info['offline'] = offline
    if args.site == 'atcoder':
        info['url'] = 'https://atcoder.jp/contests/{contest}/tasks/{contest}_{{id}}'.format(
            contest=args.contest)
    elif args.site == 'codeforces':
        info['url'] = 'https://codeforces.com/contest/{contest}/problem/{{id}}'.format(
            contest=args.contest)
    elif args.site == 'opencup':
        pass
    else:
        raise Exception()
    toml.dump(info, open(base / 'info.toml', 'w'))



def command_test(args):
    info = toml.load('info.toml')
    pdir = Path(args.problem)
    build(pdir)
    cmd = []
    if info['offline']:
        cmd = ['oj', 't', '-c', './main', '-d', './test']
    else:
        cmd = ['oj', 't', '-c', './main']
        url = info['url'].format(id=pdir.name)
        if not (pdir / "test").exists():
            check_call(['oj', 'd', url], cwd=pdir)
    run(cmd, cwd=pdir)


def command_submit(args):
    pdir = Path(args.problem)    
    check_call([str(algbase / 'expander/expander.py'), 'main.cpp', 'main_combined.cpp'], cwd=pdir)
    check_call(['oj', 's', 'main_combined.cpp', '--no-open', '-w', '0'], cwd=pdir)


if __name__ == "__main__":
    basicConfig(
        level=getenv('LOG_LEVEL', 'DEBUG'),
        format="%(asctime)s %(levelname)s %(name)s : %(message)s"
    )

    parser = argparse.ArgumentParser(epilog='''\
init example:        
  supporter.py i atcoder agc001 {a..f}
  supporter.py i codeforces 1025 {A..F}
  supporter.py i opencup 12345 {A..K}''', formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers()

    # init
    parser_init = subparsers.add_parser('i', help='init command')
    parser_init.add_argument('site', help='Contest Site(atcoder)')
    parser_init.add_argument('contest', help='Contest Name(agc001)')
    parser_init.add_argument('problems', nargs='+',
                             help='Problem Names({a..f})')
    parser_init.set_defaults(handler=command_init)

    # build
#    parser_build = subparsers.add_parser('b', help='build command')
#    parser_build.add_argument('source', help='Problem Name')
#    parser_build.set_defaults(handler=command_build)

    # test
    parser_test = subparsers.add_parser('t', help='test command')
    parser_test.add_argument('problem', help='Problem Name')
    parser_test.set_defaults(handler=command_test)

    # submit
    parser_submit = subparsers.add_parser('s', help='submit command')
    parser_submit.add_argument('problem', help='Problem Name')
    parser_submit.set_defaults(handler=command_submit)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
