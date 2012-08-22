#!/usr/bin/env python
import os.path
from glob import glob
from dulwich import repo
import mercurial.commands as hg
from mercurial import ui, localrepo
import markdown as md
import hashlib
from config_parser import configure
# TODO:
#   - cache all wiki levels (for x in os.walk...)


@configure
class Doc(object):
    def __init__(self):
        # create folders and repo if don't exist
        self.renderers = {'copy': self.render_copy, 'md': self.render_md}
        self.r = {}
        #ensure cache folder is created
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        #ensure doc folder is created
        #ensure repo is initiated
        if self.repo_root:
            if self.git_repos:
                for _repo in self.git_repos:
                    if not os.path.exists(self.repo_root + _repo):
                        os.makedirs(self.repo_root + _repo + self.doc)
                    if not os.path.exists(self.cache_path + _repo):
                        os.makedirs(self.cache_path + _repo)
                    try:
                        self.r[_repo] = repo.Repo(self.repo_root + _repo)
                    except:
                        self.r[_repo] = repo.Repo.init(
                                self.repo_root + _repo)
            if self.hg_repos:
                for _repo in self.hg_repos:
                    if not os.path.exists(self.repo_root + _repo):
                        os.makedirs(self.repo_root + _repo + self.doc)
                    if not os.path.exists(self.cache_path + _repo):
                        os.makedirs(self.cache_path + _repo)
                    try:
                        self.r[_repo] = localrepo.localrepository(
                                ui.ui(),
                                self.repo_root + _repo)
                    except:
                        hg.init(ui.ui(), self.repo_root + _repo)
                        self.r[_repo] = localrepo.localrepository(
                                ui.ui(),
                                self.repo_root + _repo)

    def render(self, filename, project, file_type='copy'):
        if file_type not in self.renderers.keys():
            file_type = 'copy'
        _doc_path = self.repo_root + project + self.doc
        with open(_doc_path + filename, 'r') as _f:
            content = _f.read()
            return(self.renderers[file_type](content))

    def render_md(self, content):
        """outputs html from markdown"""
        return(md.markdown(content, ['fenced_code', 'tables', 'codehilite']))

    def render_copy(self, content):
        """Stupid document"""
        #content = content.replace('\n', '<BR/>\n')
        return(content)

    def cache(self, filename, project):
        """caches renders in cache/"""
        _cache_path = self.cache_path + project
        _file_type = filename.rsplit('.', 1)
        if len(_file_type) > 1:
            _file_type = _file_type[1]
        else:
            _file_type = None
        if _file_type in self.renderers:
            _cache_filename = os.path.basename(filename).rsplit('.', 1)[0]
        else:
            _cache_filename = os.path.basename(filename)
        content = self.render(filename, project, _file_type)
        #get md5 of old content
        _old_md5 = hashlib.md5()
        _to_cache = "{0}/{1}".format(_cache_path, _cache_filename)
        if os.path.exists(_to_cache):
            with open(_to_cache, 'r') as _f:
                _old_md5.update(_f.read())
        #get md5 of new content
        _new_md5 = hashlib.md5()
        _new_md5.update(content)
        #if same, do nothing
        #else render the new file
        if _old_md5.hexdigest() != _new_md5.hexdigest():
            with open("{0}/{1}".format(
                _cache_path,
                _cache_filename),
                'w') as _f:
                _f.writelines(content)

    def cache_all(self):
        """caches all files"""
        for r in self.r.keys():
            for x in glob(self.repo_root + r + self.doc + "/*.*"):
                self.cache(os.path.basename(x), r)

    def list_pages(self, project):
        """list wiki pages"""
        _pages_list = []
        for x in glob(self.repo_root + project + self.doc + "/*.*"):
            _file_type = os.path.basename(x).rsplit('.', 1)[1]
            if _file_type in self.renderers:
                _pagename = os.path.basename(x).rsplit('.', 1)[0]
                _pages_list.append(_pagename)
        return(_pages_list)

    def save(self, filename, newcontent, project):
        """save newcontent in path"""
        with open(self.repo_root + project + self.doc + "/" + filename, "w") as _f:
            _f.writelines(newcontent)

    def commit(self, filename, project):
        """commit the path"""
        _path = self.repo_root + self.doc + filename
        #dulwich uses relative path
        if type(self.r[project]) == repo.Repo:
            _path = _path.lstrip(self.repo_root)
            self.r[project].stage(_path)
            self.r[project].do_commit(
                message='commit wiki page {0}'.format(filename))
        elif type(self.r[project]) == localrepo.localrepository:
            hg.add(ui.ui(), self.r, _path)
            hg.commit(
                ui.ui(),
                self.r,
                _path,
                message='commit wiki page {0}'.format(filename))


if __name__ == '__main__':
    d = Doc()
    print("render ../doc/Versioning.md")
    print(d.render('Versioning.md'))
    print("cache ../doc/Versioning.md to ../doc/cache/blah")
    d.cache('Versioning.md')
    print("cache ../doc/*.*")
    d.cache_all()
    d.save("bleurf.md", """= Hello =\n* blah\n""")
