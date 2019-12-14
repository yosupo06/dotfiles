#!/usr/bin/env python3

import os
import argparse
import shutil
import toml
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
    cxxargs.extend(['-fsanitize=address,undefined'])
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
    import onlinejudge

    contest = onlinejudge.dispatch.contest_from_url(args.url)
    offline = (contest is None)
    base = None
    if isinstance(contest, onlinejudge.service.atcoder.AtCoderContest):
        base = Path.cwd() / ('atcoder-' + contest.contest_id)
    base.mkdir()

    src = algbase / "src/base.cpp"

    for prob in args.problems:
        pdir = base / prob
        pdir.mkdir()
        shutil.copy(str(src), pdir / "main.cpp")
        if offline:
            cdir = pdir / 'test'
            cdir.mkdir()

    info = dict()
    info['offline'] = offline
    info['contest_url'] = args.url
    toml.dump(info, open(base / 'info.toml', 'w'))

def get_url(info, problem):
    if problem in info.get('url_buffer', []):
        return info['url_buffer'][problem]
    url = info['contest_url']
    
    import onlinejudge
    
    contest = onlinejudge.dispatch.contest_from_url(url)
    if not contest:
        logger.error(
            'No contest check contest_url of info.toml: {}'.format(url))
        raise
    for p in contest.list_problems():
        purl = p.get_url()
        if purl.lower().endswith(problem.lower()):
            logger.info('Problem name {} -> {}'.format(problem, p.problem_id))
            if 'url_buffer' not in info:
                info['url_buffer'] = dict()
            info['url_buffer'][problem] = purl
            toml.dump(info, open('info.toml', 'w'))
            return purl
    else:
        logger.error('No problem: {}'.format(problem))


def command_build(args):
    src = Path(args.source)
    if src.is_dir():
        src /= 'main.cpp'
    build(src)


def command_test(args):
    pdir = Path(args.problem)
    info = toml.load('info.toml')
    build(pdir / 'main.cpp')
    if not info['offline']:
        url = get_url(info, pdir.name)
        if not (pdir / "test").exists():
            logger.info('download')
            check_call(['oj', 'd', url], cwd=pdir)

    cmd = []
    if info['offline']:
        cmd = ['oj', 't', '-c', './main', '-d', './test']
    else:
        cmd = ['oj', 't', '-c', './main']
    run(cmd, cwd=pdir)


def command_submit(args):
    pdir = Path(args.problem)
    info = toml.load('info.toml')
    url = get_url(info, pdir.name)
    check_call([str(algbase / 'expander/expander.py'),
                'main.cpp', 'main_combined.cpp'], cwd=pdir)
    if info['offline']:
        pass
    else:
        check_call(['oj', 's', 'main_combined.cpp',
                    '--no-open', '-w', '0'], cwd=pdir)


if __name__ == "__main__":
    basicConfig(
        level=getenv('LOG_LEVEL', 'INFO'),
        format="%(message)s"
    )

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # init
    parser_init = subparsers.add_parser('i', help='init command', epilog='''\
init example:
  supporter.py i https://atcoder.jp/contests/abc147 {A..F}
  ''', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_init.add_argument('url', help='Contest URL')
    parser_init.add_argument('problems', nargs='+',
                             help='Problem Names({a..f})')
    parser_init.set_defaults(handler=command_init)

    # build
    parser_build = subparsers.add_parser('b', help='build command')
    parser_build.add_argument('source', help='Source/Folder Name')
    parser_build.set_defaults(handler=command_build)

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
