#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import sys
sys.path.extend(['lib'])
from cork import Cork
from cleanup import Orgapp
import os


def l2w(_d, dico, idx=1):
    """ Converts a list of path, to an entry similar to os.walk"""
    #'/app/config/config-example.ini'
    _p = os.path.split(_d)
    #[ /app/config, config-example.ini ]
    dico[_p[0]] = dico.get(_p[0], [set(), set()])
    #{ '/app/config': [ [], [] ] }
    if _p[1] != '':
        dico[_p[0]][idx].add(_p[1])
    _path = os.path.split(_p[0])
    if _path[1] != '':
        dico[_path[0]] = dico.get(_path[0], [set(), set()])
        dico[_path[0]][0].add(_path[1])
        l2w(_path[0], dico, idx=0)

auth = Cork('config')
o = Orgapp(
    statuses=['backlog', 'new', 'running', 'done'])
