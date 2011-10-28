#!/usr/bin/env python
import os
from bottle import route, run, static_file
from bottle import view, template
from bottle import get, post, request, error

@route('/')
@view('base')
def home(page='home'):
    return dict(content='Hello, how are you?',
                page=page)

@route('/wiki/')
@route('/wiki/:page#.+#')
@view('wiki_2col')
def wiki(page=''):
  fullpath = './wiki/%s' % page
  if not os.path.isfile(fullpath):
    if os.path.isdir(fullpath):
      files = os.listdir(fullpath)
      dirname = fullpath
      if os.path.exists(fullpath+'index'): page = page + 'index'
      else: page = page +'/'+ files[0]
    else:
      dirname = '/wiki'
  else: 
    files = os.listdir(os.path.dirname(fullpath))
    dirname = os.path.dirname(fullpath)
  print('='*10)
  print(page)
  print('='*10)
  if not page: page = 'index' 
  input_str = static_file(page, root='./wiki').output.read().decode().replace('\n','<br/>')
  try:
    import docutils
  except Exception as e:
    return dict(page=page,content=input_str, files=files, path=dirname)
  else:
    return dict(page=page+"_docutils",content=input_str, files=files, path=dirname)

@route('/static/:filename#.+#')
def server_static(filename):
    return static_file(filename, root='./static')

@error(404)
def error404(error):
    return 'you might be looking for something you won\'t get'

import bottle
bottle.debug(True)
run(host='localhost', port=8080,reloader=True)
#run(host='172.16.0.163', port=8080)
