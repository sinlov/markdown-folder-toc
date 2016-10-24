#!/usr/bin/env python
# coding=utf-8

#####################################################
# ghtoc   : markdown folder toc generator
# Author  : sinlov <sinlovgmppt@gmail.com>
# Usage   : toc.py <markdown file>
# Date    : 2016-10-24
# License : see https://github.com/sinlov/markdown-folder-toc
# Copyright (C) 2016 sinlov
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
__author__ = 'sinlov'
import os
import re
import sys
import shutil

top_level = 77
folder_deep = 5
lnk_temp = '%s- [%s](%s#%s)'
TOC_MARK = '--------------'
REG_TOC_MARK = r'--------------'
REF = '**Folder TOC generated by [sinlov](https://github.com/sinlov/markdown-folder-toc)**'

help_info = """
Welcome use Markdown Folder TOC generate
    Usage:
        ./folder_toc.py <markdown folder>
    You can also use -d to set generate deep
        ./folder_toc.py -d 3 <markdown folder>

    -d folder deep default 5
    -l top level default 77

more information see https://github.com/sinlov/markdown-folder-toc
"""

error_info = """
Your input error
    Usage:
        ./folder_toc.py <markdown folder>
    or input [-h] to see help
"""

data = {"default": []}


def load():
    if len(sys.argv[1:]) == 0: return False
    key = "default"
    for raw in sys.argv[1:]:
        if raw.startswith("-"):
            key = raw
            if key not in data: data[key] = []
        else:
            data[key].append(raw)
    return True


def read(*args):
    if len(args) == 0: return _getVal("default")
    for key in args:
        if key in data: return _getVal(key)
    return None


def readList(*args):
    if len(args) == 0: return data["default"]
    for key in args:
        if key in data: return data[key]
    return None


def _getVal(key): return data[key][0] if len(data[key]) > 0 else ""


# def get_cur_dir():
#     global __CUR_DIR
#     ret_path = __CUR_DIR
#     if sys.platform.system() == 'Windows':
#         ret_path = ret_path.decode('gbk')
#     return ret_path
#     caller_file = inspect.stack()[0][1]
#     ret_path = os.path.abspath(os.path.dirname(caller_file))
#     if platform.system() == 'Windows':
#         ret_path = ret_path.decode('gbk')
#     return ret_path


# def get_full_path(filename):
#     filename = filename.replace('\\', '/')
#     # filename = re.sub('/+', '/', filename)
#     if os.path.isabs(filename):
#         return filename
#     dir_name = get_cur_dir()
#     filename = os.path.join(dir_name, filename)
#     filename = filename.replace('\\', '/')
#     filename = re.sub('/+', '/', filename)
#     return filename


def auto_move_toc(full):
    result = []
    not_toc = True
    for line in full:
        if re.match(REG_TOC_MARK, line):
            not_toc = not not_toc
            continue
        elif not_toc:
            result.append(line)
    return result


def tr_toc(header, file_name=str):
    global lnk_temp
    lvl, txt = re.findall(r'^(\d+) (.*)', header)[0]
    return lnk_temp % (
        (int(lvl) - top_level) * '    ', txt, file_name, re.sub(' ', '-', re.sub('[^-a-z0-9 ]', '', txt.lower())))


def generate_file_toc(root=str, root_len=int, f_name=str, save_name=str):
    global top_level
    lines = []
    with open(os.path.join(root, f_name), 'r') as file:
        lines = file.readlines()
        if len(lines) == 0:
            print 'You file is empty, please check it!'
            return
    newlines = auto_move_toc(lines)
    file_toc = [e.strip() for e in newlines if re.match(r'#+', e)]
    # encode TOC
    for i, h in enumerate(file_toc):
        ln = len(re.search(r'^#+', h).group(0))
        top_level = ln if ln < top_level else top_level
        file_toc[i] = re.sub(r'^#+\s*', str(ln) + ' ', h)
    md_path = ''
    if root[root_len:]:
        md_path = root[root_len:] + '/' + f_name
    else:
        md_path = f_name
    file_toc = [tr_toc(h, md_path) for h in file_toc]
    # write in file
    with open(save_name, 'a') as f:
        f.write('\n'.join(file_toc) + '\n')
        # f.write(''.join(newlines))
        f.write('\n')


def generate_markdown_folder(root_path=str):
    global folder_deep
    if os.path.exists(save_path):
        os.remove(save_path)
    print "=== Save path ===\nas: " + save_path + '\n'
    if folder_deep != 5:
        print 'folder level change as: ' + str(folder_deep) + '\n'
    now_folder_deep = 1
    root_len = len(root_path)
    for root, dirs, files in os.walk(folder_path, True, True):
        for name in files:
            if name.endswith(".md") and folder_deep >= now_folder_deep:
                print("Find markdown file at: " + os.path.join(root, name))
                generate_file_toc(root, root_len, name, save_path)
        for name in dirs:
            now_folder_deep += 1
            # print  'folder_deep: ' + str(folder_deep) + ' |now_folder_deep ' + str(now_folder_deep)
    with open(save_path, 'a') as f:
        f.write('\n' + TOC_MARK)
        f.write('\n\n\n')
        f.write(REF)
        f.write('\n\n')


if __name__ == '__main__':
    folder_path = ''
    load()
    is_check_args = False
    # filter args start
    if read('-h'):
        print help_info
        exit(0)
    if len(sys.argv) == 1:
        folder_path = os.getcwd()
        print 'You want make toc at ' + folder_path
        is_check_args = True
    elif read('-l'):
        top_level = read('-l')
        is_check_args = True
    elif read('-d'):
        folder_deep = int(read('-d'))
        is_check_args = True
    if read():
        folder_path = os.getcwd() + '/' + read()
        is_check_args = True
    # filter args end
    if read('-e') is None and len(sys.argv) > 2 and not is_check_args:
        print error_info
        exit(-1)
    # check args finish
    if not os.path.exists(folder_path):
        print "Your input Folder is not exist " + folder_path
        exit(-1)
    if os.path.isdir(folder_path) < 1:
        print "You input " + folder_path + "is not folder"
        exit(-2)
    # check folder path finish
    save_path = os.path.realpath(folder_path) + "/preface.md"
    generate_markdown_folder(folder_path)
    print '=== folder generate success! ===\nSee at ' + save_path
