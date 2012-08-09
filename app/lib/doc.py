#!/usr/bin/env python
import os.path
from glob import glob
from dulwich import repo
import markdown as md
import hashlib
# TODO:
#   - cache all wiki levels (for x in os.walk...)


class Doc():
    def __init__(self):
        # create folders and repo if don't exist
        self.renderers = {'copy': self.render_copy, 'md': self.render_md}
        self.r = repo.Repo('../')

    def render(self, filename, file_type='copy'):
        if file_type not in self.renderers.keys():
            file_type = 'copy'
            with open(filename, 'r') as _f:
                content = _f.read()
                return(self.renderers[file_type](content))

    def render_md(self, content):
        """outputs html from markdown"""
        return(md.markdown(content, ['fenced_code', 'tables', 'codehilite']))

    def render_copy(self, content):
        """Stupid document"""
        #content = content.replace('\n', '<BR/>\n')
        return(content)

    def cache(self, filename):
        """caches renders in cache/"""
        _cache_path = os.path.dirname(filename)
        _file_type = os.path.basename(filename).rsplit('.', 1)[1]
        if _file_type in self.renderers:
            _cache_filename = os.path.basename(filename).rsplit('.', 1)[0]
        else:
            _cache_filename = os.path.basename(filename)
            content = self.render(filename, _file_type)
            #get md5 of old content
            _old_md5 = hashlib.md5()
            _to_cache = "{0}/cache/{1}".format(_cache_path, _cache_filename)
            if os.path.exists(_to_cache):
                with open(_to_cache, 'r') as _f:
                    _old_md5.update(_f.read())
                    #get md5 of new content
                    _new_md5 = hashlib.md5()
                    _new_md5.update(content)
                    #if same, do nothing
                    #else render the new file
                    if _old_md5.hexdigest() != _new_md5.hexdigest():
                        _f = open("{0}/cache/{1}".format(
                            _cache_path,
                            _cache_filename),
                            'w')
                        _f.writelines(content)
                        _f.close()

    def cache_all(self, path):
        """caches all files"""
        for x in glob(path):
            self.cache(x)

    def list_pages(self, path):
        """list wiki pages"""
        _pages_list = []
        for x in glob(path):
            print(os.path.basename(x).rsplit('.', 1))
            _file_type = os.path.basename(x).rsplit('.', 1)[1]
            if _file_type in self.renderers:
                _pagename = os.path.basename(x).rsplit('.', 1)[0]
                _pages_list.append(_pagename)
                return(_pages_list)

    def save(self, path, newcontent):
        """save newcontent in path"""
        _f = open(path, "w")
        _f.writelines(newcontent)
        _f.close()

    def commit(self, path):
        """commit the path"""
        self.r.stage(path)
        self.r.do_commit(
            message='commit wiki page {0}'.format(os.path.basename(path)))


if __name__ == '__main__':
    d = Doc()
    print("render ../doc/Versioning.md")
    print(d.render('../doc/Versioning.md'))
    print("cache ../doc/Versioning.md to ../doc/cache/blah")
    d.cache('../doc/Versioning.md')
    print("cache ../doc/*.*")
    d.cache_all("../doc/*.*")
    d.save("../doc/bleurf.md", """= Hello =\n* blah\n""")
