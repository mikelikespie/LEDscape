#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'))
    parser.add_argument("output", type=argparse.FileType('w'))

    args = parser.parse_args()

    cpp = os.environ.get("CPP", 'clang++ -E').split()

    proc = subprocess.Popen(cpp + ['-', '-Wno-comment'], stdin=args.input, stdout=subprocess.PIPE)
    for l in proc.stdout:
        if l.startswith('#'):
            continue

        args.output.write(l.replace(';', '\n'))

    if proc.wait() != 0:
        raise Exception("Proc failed")

    args.output.flush()
    args.output.close()

if __name__ == '__main__':
    main()



