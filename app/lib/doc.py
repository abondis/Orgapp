#!/usr/bin/env python
import os.path
from glob import glob
from dulwich import repo
import markdown as md
import hashlib
# stupid plain text one level wiki
# TODO:
#   - cache other files
#   - cache all wiki levels (for x in os.walk...)


def render(filename, file_type='copy'):
  if file_type not in renderers.keys():
    file_type = 'copy'
  with open(filename, 'r') as _f:
    content = _f.read()
  return(renderers[file_type](content))

def render_md(content):
  """outputs html from markdown"""
  return(md.markdown(content, ['fenced_code', 'tables', 'codehilite']))

def render_copy(content):
  """Stupid document"""
  #content = content.replace('\n', '<BR/>\n')
  return(content)

def cache(filename):
  """caches renders in cache/"""
  _cache_path = os.path.dirname(filename)
  _file_type = os.path.basename(filename).rsplit('.', 1)[1]
  if _file_type in renderers:
    _cache_filename = os.path.basename(filename).rsplit('.', 1)[0]
  else:
    _cache_filename = os.path.basename(filename)
  content = render(filename, _file_type)
  #get md5 of old content
  _old_md5 = hashlib.md5()
  _to_cache = "{0}/cache/{1}".format(_cache_path,_cache_filename)
  if os.path.exists(_to_cache):
    with open(_to_cache, 'r') as _f:
      _old_md5.update(_f.read())
  #get md5 of new content
  _new_md5 = hashlib.md5()
  _new_md5.update(content)
  #if same, do nothing
  #else render the new file
  if _old_md5.hexdigest() != _new_md5.hexdigest(): 
    print("caching {0}".format(os.path.basename(filename)))
    print("old: {0}, new: {1}".format(_old_md5.hexdigest(), _new_md5.hexdigest()))
    _f = open("{0}/cache/{1}".format(_cache_path,_cache_filename), 'w')
    _f.writelines(content)
    _f.close()

def cache_all(path):
  """caches all files"""
  for x in glob(path):
    cache(x)

def save(path, newcontent):
  """save newcontent in path"""
  _f = open(path, "w")
  _f.writelines(newcontent)
  _f.close()

def commit(path):
  """commit the path"""
  r.stage(path)
  r.do_commit(
    message='commit wiki page {0}'.format(os.path.basename(path)))

renderers = { 'copy': render_copy, 'md': render_md }
r = repo.Repo('../')

if __name__ == '__main__':
  print("render ../doc/Versioning.md")
  print(render('../doc/Versioning.md'))
  print("cache ../doc/Versioning.md to ../doc/cache/blah")
  cache('../doc/Versioning.md')
  print("cache ../doc/*.*")
  cache_all("../doc/*.*")
  save("../doc/bleurf.md", """= Hello =\n* blah\n""")
