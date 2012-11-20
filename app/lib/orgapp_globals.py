#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import sys
sys.path.extend(['lib'])
from cork import Cork
from cleanup import *
from bottle import run, static_file, request
from bottle import view, redirect, template, url
from bottle import post, get
from bottle import app
#from tasks import Tasks
#from cleanup import Tasks
#from cleanup import Statuses
#from cleanup import Projects


auth = Cork('config')
p = Orgapp('/tmp/projects', ['test', 'truc', 'unknown'])
