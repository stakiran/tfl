# encoding: utf-8

import glob
import os
import re
import sys

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('-d', '--dir', default='./',
        help='A target directory. If omitted then use the current dir.')

    parser.add_argument('--use-target', default=False, action='store_true',
        help='If given then use output format `-target=resourcetype.name`.')

    args = parser.parse_args()
    return args

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

RE_resource = re.compile(r'([a-zA-Z0-9_\-]+)')

class TerraformFile:
    def __init__(self, filepath, lines):
        self._filepath = filepath

        self._resources = {}

        self._parse(lines)

    def _parse(self, lines):
        self._lines = lines

        for line in lines:
            self._parse_line(line)

    def _parse_line(self, line):
        if line.startswith('resource'):
            self._parse_as_resource(line)
            return

    def _parse_as_resource(self, line):
        elms = re.findall(RE_resource, line)

        try:
            _, type, name = elms
        except ValueError as e:
            msg = '{}\nfile: {}\nelements: {}'.format(
                str(e),
                self.filepath,
                elms,
            )
            abort(msg)
        if not type in self._resources:
            self._resources[type] = []
        self._resources[type].append(name)

    @property
    def resources(self):
        return self._resources

    @property
    def filepath(self):
        return self._filepath

class Merger:
    def __init__(self, tffile_insts):
        self._insts = tffile_insts

        self._merge_resources()

    def _merge_resources(self):
        self._resources = {}

        for inst in self._insts:
            for type in inst.resources:
                if not type in self._resources:
                    self._resources[type] = []
                self._resources[type].extend(inst.resources[type])

    @property
    def resources(self):
        return self._resources

def output_normal(merger):
    outlines = []
    for type in merger.resources:
        outlines.append('# {}'.format(type))
        names = merger.resources[type]
        for name in names:
            outlines.append('- {}'.format(name))
        outlines.append('')
    return outlines

def output_target_format(merger):
    outlines = []
    for type in merger.resources:
        names = merger.resources[type]
        for name in names:
            outline = '-target={}.{}'.format(type, name)
            outlines.append(outline)
    return outlines

def output(tffile_insts, use_target):
    merger = Merger(tffile_insts)

    if use_target:
        outlines = output_target_format(merger)
    else:
        outlines = output_normal(merger)

    for line in outlines:
        print(line)

if __name__ == "__main__":
    args = parse_arguments()
    basedir = args.dir

    tffiles = get_tffiles_nestly(basedir)
    tffile_insts = []
    for i,tffile in enumerate(tffiles):
        correct_path = os.path.join(basedir, tffile)
        lines = file2list(correct_path)
        inst = TerraformFile(tffile, lines)
        tffile_insts.append(inst)

    output(tffile_insts, args.use_target)
