#!/usr/bin/env python
import os.path as path
# stupid plain text one level wiki
# TODO:
#   - cache other files
#   - cache all wiki levels (for x in os.walk...)

def render(filename):
  """Stupid document, replaces \n with <BR/>"""
  _f = open(filename, 'r')
  _datas = _f.read()
  _datas = _datas.replace('\n', '<BR/>\n')
  _f.close()
  return(_datas)

def cache(filename):
  """caches renders in cache/"""
  #cache filename
  _cache_filename = filename.rsplit('.', 1)[0]
  _f = open("cache/{0}.html".format(_cache_filename), 'w')
  _f.writelines(render(filename))
  _f.close()

if __name__ == '__main__':
  print("render blah.t2t")
  print(render('blah.t2t'))
  print("cache blah.t2t to cache/blah.html")
  cache('blah.t2t')
