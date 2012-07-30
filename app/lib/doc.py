#!/usr/bin/env python
import os.path as path
from glob import glob
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
  _cache_path = path.dirname(filename)
  #cache filename
  _cache_filename = path.basename(filename).rsplit('.', 1)[0]
  _f = open("{0}/cache/{1}.html".format(_cache_path,_cache_filename), 'w')
  _f.writelines(render(filename))
  _f.close()

def cache_all(path):
  """caches all files"""
  for x in glob(path):
    cache(x)


if __name__ == '__main__':
  print("render blah.t2t")
  print(render('blah.t2t'))
  print("cache blah.t2t to cache/blah.html")
  cache('blah.t2t')
  print("cache *.t2t")
  cache_all("*.t2t")
