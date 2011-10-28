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
@view('block_content')
def wiki(page=''):
  files = os.listdir(os.path.dirname('./wiki/%s' % page))
  if not page: page = 'index' or files[0]
  input_str = static_file(page, root='./wiki').output.read().decode().replace('\n','<br/>')
  try:
    import docutils
  except Exception as e:
    return dict(page=page,content=input_str, files=files)
  else:
    return dict(page=page+"_docutils",content=input_str, files=files)

@route('/static/:filename#.+#')
def server_static(filename):
    return static_file(filename, root='./static')

@error(404)
def error404(error):
    return 'you might be looking for something you won\'t get'


run(host='localhost', port=8080)
#run(host='172.16.0.163', port=8080)
