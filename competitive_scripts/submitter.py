#!/usr/bin/env python3
from atcodertools.client.models.contest import Contest
from atcodertools.client.atcoder import AtCoderClient

cid = ''
with open('ID.txt') as f:
    cid = f.read().strip()

print('Contest ID = {}'.format(cid))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('problemid', help='problem id')
args = parser.parse_args()
pid = args.problemid

try:
    at = AtCoderClient()
    at.login()
    cn = Contest(cid)
    pls = at.download_problem_list(cn)

except Exception as e:
    print('ログイン/問題取得でエラー Exception = {}'.format(e))

else:
    for pl in pls:
        k = pl.alphabet
        if k != pid and pid != 'all':
            continue
        v = pl.get_url()

        try:
            src = ''
            with open('../{}.cpp'.format(k)) as f:
                src = f.read()
            at.submit_source_code(cn, pl, 'C++14 (GCC 5.4.1)', src)
        except Exception as e:
            print('Submit Failed {} Exception = {}'.format(k, e))

        if args.problemid != 'all':
            break
    else:
        print('No Problem {}'.format(pid))