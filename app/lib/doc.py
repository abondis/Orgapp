#!/usr/bin/env python
import os.path
from glob import glob
import markdown as md
# stupid plain text one level wiki
# TODO:
#   - cache other files
#   - cache all wiki levels (for x in os.walk...)


def render(filename, file_type='txt'):
  if file_type not in renderers.keys():
    file_type = 'txt'
  _f = open(filename, 'r')
  content = _f.read()
  _f.close()
  return(renderers[file_type](content))

def render_md(content):
  """outputs html from markdown"""
  return(md.markdown(content))

def render_txt(content):
  """Stupid document, replaces \n with <BR/>"""
  content = content.replace('\n', '<BR/>\n')
  return(content)

def cache(filename):
  """caches renders in cache/"""
  _cache_path = os.path.dirname(filename)
  #cache filename
  print("caching {0}".format(os.path.basename(filename)))
  _file_type = os.path.basename(filename).rsplit('.', 1)[1]
  _cache_filename = os.path.basename(filename).rsplit('.', 1)[0]
  _f = open("{0}/cache/{1}".format(_cache_path,_cache_filename), 'w')
  _f.writelines(render(filename, _file_type))
  _f.close()

def cache_all(path):
  """caches all files"""
  for x in glob(path):
    print(os.path.basename(x))
    _file_type = os.path.basename(x).rsplit('.', 1)[1]
    if _file_type in renderers.keys():
      cache(x)

renderers = { 'txt': render_txt, 'md': render_md }

if __name__ == '__main__':
  print("render ../doc/blah.md")
  print(render('../doc/blah.md'))
  print("cache ../doc/blah.md to ../doc/cache/blah")
  cache('../doc/blah.md')
  print("cache ../doc/*.*")
  cache_all("../doc/*.*")
