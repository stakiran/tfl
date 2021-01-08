# encoding: utf-8

import glob
import os
import sys

def abort(msg):
    print('Error!: {0}'.format(msg))
    exit(1)

def file2list(filepath):
    ret = []
    with open(filepath, encoding='utf8', mode='r') as f:
        ret = [line.rstrip('\n') for line in f.readlines()]
    return ret

def list2file(filepath, ls):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.writelines(['{:}\n'.format(line) for line in ls] )

def file2str(filepath):
    ret = ''
    with open(filepath, encoding='utf8', mode='r') as f:
        ret = f.read()
    return ret

def str2file(filepath, s):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.write(s)

def get_tffiles_nestly(target_abs_path):
    query = '{}/**/*.tf'.format(target_abs_path)
    files = glob.glob(query, recursive=True)

    newlines = []
    for file_abs in files:
        file_relative = file_abs.replace(target_abs_path, '')
        if file_relative[0] == '\\':
            file_relative = file_relative[1:]
        newlines.append(file_relative)

    return newlines

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('-d', '--dir', default='./',
        help='A target directory. If omitted then use the current dir.')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()

    tffiles = get_tffiles_nestly(args.dir)
    for tffile in tffiles:
        print(tffile)
