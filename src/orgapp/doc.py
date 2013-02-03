#
#This file is part of Orgapp.
#
#Orgapp is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Orgapp is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Orgapp.  If not, see <http://www.gnu.org/licenses/>.

import os
import markdown as md


class Doc:
    """Handle documents"""
    def __init__(self, root_path, cache_path):
        self.renderers = {'copy': self.render_copy, '.md': self.render_md}
        self.root_path = root_path
        self.cache_path = cache_path
        ## create doc dir
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        # create doc cache dir
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        for _f in self.files_list(self.root_path):
            self.cache(_f)

    def is_static(self, path):
        """Verifies if the file is just a copy or a render"""
        return os.path.exists(self.cache_path + path)

    def cache_list(self):
        return self.files_list(self.cache_path)

    def files_list(self, path):
        """List files contained in a Doc instance"""
        print path
        print os.listdir(path)
        return sorted(os.listdir(path))

    def get_file_ext(self, path):
        return os.path.splitext(path)[1]

    def get_doc(self, filename, cache=True):
        if cache:
            path = self.cache_path
        else:
            path = self.root_path
        with open(path + '/' + filename) as _f:
            return _f.read()

    def create_doc(self, filename, content, mode='doc'):
        """ creates a document using some content
        mode: is doc by default, can be cache to use the cache_path instead
        of root_path
        """
        if mode == 'doc':
            path = self.root_path
        elif mode == 'cache':
            path = self.cache_path
        with open(path + '/' + filename, 'w') as _f:
            _f.write(content)

    def cache(self, filename):
        """cache creates files with no extension"""
        content = self.render(filename)
        cached_filename = os.path.splitext(filename)[0]
        self.create_doc(cached_filename, content, mode='cache')

    def render(self, filename):
        """renders a doc into cache_path.
        Let project handle path construction"""
        _ext = self.get_file_ext(filename)
        print 'our ext' + _ext
        if _ext not in self.renderers.keys():
            _ext = 'copy'
        with open(self.root_path + '/' + filename, 'r') as _f:
            content = _f.read()
        return(self.renderers[_ext](content))

    def render_copy(self, content):
        return content

    def render_md(self, content):
        return(md.markdown(content, ['fenced_code', 'tables', 'codehilite']))
