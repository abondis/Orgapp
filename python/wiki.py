#!/usr/bin/env python2
import os
try:
  import io
except:
  import StringIO 
  io = StringIO
try:
  import textile
except Exception:
  pass
from bottle import route, run, static_file, redirect
from bottle import view, template
from bottle import get, post, request, error

@route('/home')
def home():
  return redirect('/')

@route('/')
@view('base')
def home(page='home'):
    return dict(content='<p>Hello, how are you?</p>',
                page=page)

def render_textile(raw):
  return textile.textile(raw)

def wiki_url():
  """
    populates dic path2title and title2path.
    path2title: gives a set (title, titlePath) for every path in the wiki
    title2path: gives a set (fileName, filePath) for every niceURL
  """
  title2path = {}
  path2title = {}
  for i in os.walk('wiki'):
    for j in i[2]:
      filePath = str.strip(i[0]+'/'+j, '\n')
      fileName = str.strip(j, '\n')
      f = open(filePath, 'r')
      title = f.readline()
      titlePath = str.strip(i[0]+'/'+title, '\n')
      f.close
      path2title[filePath] = (title, titlePath)
      title2path[titlePath] = (fileName, filePath)
    # set key for folders
    if len(i[2]):
#      print("i[0]: %s/ i[2]: %s" % (i[0],i[2]))
      path2title[i[0]+'/'] =  path2title[i[0]+'/'+i[2][0]]
      path2title[i[0]] =  path2title[i[0]+'/'+i[2][0]]
      title2path[i[0]+'/'] = title2path[path2title[i[0]+'/'+i[2][0]][1]]
      title2path[i[0]] = title2path[path2title[i[0]+'/'+i[2][0]][1]]
  return title2path, path2title

@route('/wiki')
@route('/wiki/')
@route('/wiki/:page#.+#')
@view('wiki_2col')
def wiki(page=''):
  # /wiki/machin/blah blah blah
  # -> fullpath = /wiki/machin/blah.txt
  # -> <a href=path2title['fullpath']['1']>title</a>
  page, fullpath = title2path['wiki/%s' % page]
  if os.path.isdir(fullpath):
    files = os.listdir(fullpath)
    dirname = fullpath
  else:
    dirname = os.path.dirname(fullpath)
    files = os.listdir(dirname)

  if not page: page = 'index' 
  print("page: %s, fullpath: %s, dirname: %s" % (page, fullpath, dirname))
  print(static_file(page, root=dirname).output)
  input_str = static_file(page, root=dirname).output.read()
  try:
    import textile
  except Exception:
    input_str = input_str.decode().replace('\n','<br/>')
    return dict(page=page,content=input_str, files=files, path=dirname)
  else:
    return dict(page=page+"_textile",content=render_textile(input_str), files=files, path=dirname, t2p=title2path, p2t=path2title)

@route('/tasks')
@route('/tasks/')
@view('tasks')
def tasks():
  global tasks 
  tasks = []
  f = open('todo.txt', 'r')
  for t in f.xreadlines():
    tasks.append(t) 
  f.close()
  return dict(tasks=tasks, page="Tasks List")

@route('/static/:filename#.+#')
def server_static(filename):
    return static_file(filename, root='./static')

@error(404)
def error404(error):
    return 'you might be looking for something you won\'t get'

import bottle
bottle.debug(True)
global title2path
global path2title
#global tasks
tasks = []
(title2path, path2title) = wiki_url()
print(path2title.keys())
print(title2path.keys())
#print(path2title['wiki/linux-kernel/imac12.2-arch/linux-imac121.preset'])
run(host='localhost', port=8080,reloader=True)
#run(host='172.16.0.163', port=8080)
