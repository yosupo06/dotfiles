#!/usr/bin/env python3

import unittest
import tempfile
import shutil
from logging import basicConfig, getLogger
from os import getenv
from subprocess import PIPE, run
from pathlib import Path

logger = getLogger(__name__)


class TestBuild(unittest.TestCase):
    def test_build(self):
        proc = run(
            ['./supporter.py', 'b', 'test_src/a.cpp'])
        self.assertEqual(proc.returncode, 0)
        proc = run(['./test_src/a'])
        self.assertEqual(proc.returncode, 0)

    def test_folder_build(self):
        proc = run(
            ['./supporter.py', 'b', 'test_src/b'])
        self.assertEqual(proc.returncode, 0)
        proc = run(['./test_src/b/main'])
        self.assertEqual(proc.returncode, 0)


class TestContest(unittest.TestCase):
    def test_atcoder(self):
        tempdir = Path(tempfile.mkdtemp())
        pdir = Path(tempdir) / 'atcoder-nikkei2019-2-qual'

        logger.info('Test Contest {}'.format(tempdir))

        proc = run(
            [str(Path.cwd() / 'supporter.py'), 'i', 'https://atcoder.jp/contests/nikkei2019-2-qual', 'A'], cwd=tempdir)
        self.assertEqual(proc.returncode, 0)

        shutil.copy('test_src/nikkei2_a.cpp', pdir / 'A' / 'main.cpp')

        proc = run(
            [str(Path.cwd() / 'supporter.py'), 't', 'A'], cwd=pdir)
        self.assertEqual(proc.returncode, 0)

        proc = run(
            [str(Path.cwd() / 'supporter.py'), 't', 'A'], cwd=pdir)
        self.assertEqual(proc.returncode, 0)

if __name__ == "__main__":
    basicConfig(
        level=getenv('LOG_LEVEL', 'DEBUG'),
        format="%(asctime)s %(levelname)s %(name)s : %(message)s"
    )
    unittest.main()
