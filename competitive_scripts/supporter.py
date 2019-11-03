#!/usr/bin/env python3

import os, argparse, shutil, toml
from pathlib import Path
from subprocess import check_call, run

def build(pdir: Path):

    cxxargs = [os.getenv('CXX', 'g++')]
    cxxargs.extend(['-std=c++17'])
    cxxargs.extend(['-Wall', '-Wextra', '-Wshadow', '-Wconversion'])
    cxxargs.extend(['-DLOCAL'])

    cxxargs.extend(['-g'])
    cxxargs.extend(['-fsanitize=address,undefined', '-fno-sanitize-recover'])
    cxxargs.extend(['-fno-omit-frame-pointer'])
    cxxargs.extend(['-o', 'main'])
    cxxargs.extend(['main.cpp'])
    
    check_call(cxxargs, cwd=pdir)


def command_init(args):
    base = Path(args.site + "-" + args.contest)
    base.mkdir()

    src = Path.home() / Path("Programs/Algorithm/src/base.cpp")

    for prob in args.problems:
        pdir = base / prob
        pdir.mkdir()
        shutil.copy(str(src), pdir / "main.cpp")
    
    # make info.toml
    assert(args.site == 'atcoder')
    info = dict()
    info['url'] = 'https://atcoder.jp/contests/{contest}/tasks/{contest}_{{id}}'.format(contest=args.contest)
    toml.dump(info, open(base / 'info.toml', 'w'))
        
def get_url(pdir: Path):
    info = toml.load('info.toml')
    return info['url'].format(id=pdir.name)

def command_test(args):
    pdir = Path(args.problem)
    url = get_url(pdir)
    build(pdir)
    if not (pdir / "test").exists():
        check_call(['oj', 'd', url], cwd=pdir)        
    run(['oj', 't', '-c', './main'], cwd=pdir)


def command_submit(args):
    pdir = Path(args.problem)
    check_call(['oj', 's', 'main.cpp', '--no-open', '-w', '0'], cwd=pdir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # init
    parser_init = subparsers.add_parser('i', help='init command')
    parser_init.add_argument('site', help='Contest Site(atcoder)')
    parser_init.add_argument('contest', help='Contest Name(agc001)')
    parser_init.add_argument('problems', nargs='+', help='Problem Names({a..f})')
    parser_init.set_defaults(handler=command_init)

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

