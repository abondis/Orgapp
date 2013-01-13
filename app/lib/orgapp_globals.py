#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import sys
sys.path.extend(['lib'])
from cork import Cork
from cleanup import Orgapp
import os
from bottle import request, abort


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


def is_ajax(fn):
    def is_ajax(fn):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return fn
        else:
            abort(404, "pfff")

auth = Cork('config')
o = Orgapp(
    statuses=['backlog', 'new', 'running', 'done'])
