#!/usr/bin/env python
# -*- coding:utf-8; mode:python-mode -*-
# Last Change:2009/10/30 01:21:32.
#
# GPL v3.
#
# Copyright(c) 2009 Dai Takahashi
# All rights reserved.
#
# このスクリプトを使用した結果については一切責任をとりません。
# すべて自己責任で使用してください。
#

import sys
import os, os.path
import optparse
import re
import hashlib

HASH_MAX_BUFFER = 4096
BACKUP_EXT = '.bak'

def MakeBackup(name, new_name):
    try:
        os.rename(name, name + BACKUP_EXT)
        f_old = open(name + BACKUP_EXT, 'rb')
        x = f_old.read()
        f_old.close()

        f = open(new_name, 'wb')
        f.write(x)
        f.close()

    except Exception, e:
        print (e)
        return False

    return True


def MakeMD5(name):
    fp = open(name, 'rb')

    buf = ""
    md5 = hashlib.md5()
    while True:
        buf = fp.read( HASH_MAX_BUFFER )
        if buf:
            md5.update( buf )
        else:
            break

    return md5.digest()

if __name__ == '__main__':
    if len(sys.argv) == 1: sys.exit(1)

    usage = "usage: %prog [option] argv"
    parser = optparse.OptionParser(usage)
    parser.add_option('-e', '--ext',
                      action = "store",
                      dest = "new_ext",
                      help = "replace ext")

    (option, args) = parser.parse_args()

    for fname in args:
        (name, ext) = os.path.splitext(fname)
        new_name = name
        try:
            if option.new_ext[0] == '.':
                new_name = name + option.new_ext
            else:
                new_name = name + '.' + option.new_ext
        except Exception, e:
            print('拡張子がないので削ります。')


        if not MakeBackup(fname, new_name):
            print('Cannot make Backupfile.\nexit.')
            continue

        if MakeMD5(fname + BACKUP_EXT ) == MakeMD5(new_name):
            try:
                os.remove(fname + BACKUP_EXT)

            except Exception, e:
                print(e)
        else:
            print('%s can not rename ext.' % fname)
            try:
                os.rename(fname + BACKUP_EXT, fname)
            except Exception, e:
                print(e)
                print('Cannot rename BACKUP.\nBut File remain %s!' %s (fname + BACKUP_EXT))

