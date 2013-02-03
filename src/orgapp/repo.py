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


import mercurial.commands as hg
from mercurial import ui as hgui, localrepo as hgrepo
from dulwich import repo as gitrepo
import os
from orgapp.utils import l2w


class Repo:
    def __init__(self, path, vcs_type):
        self.ui = hgui.ui()
        self.path = path
        self.vcs_type = vcs_type
        if self.vcs_type == 'git':
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            try:
                self.r = gitrepo.Repo(self.path)
            except:
                self.r = gitrepo.Repo.init(self.path)
        elif self.vcs_type == 'hg':
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            try:
                self.r = hgrepo.localrepository(
                    self.ui,
                    self.path)
            except:
                hg.init(self.ui, self.path)
                self.r = hgrepo.localrepository(
                    self.ui,
                    self.path)

    def add_file(self, path):
        if self.vcs_type == 'git':
            # git wants a relative path
            path = path[len(self.path) + 1:]
            self.r.stage(path.encode('utf-8'))
        # FIXME: does not work if there was an
            # issue with other uncommitted things
            self.r.do_commit(
                message='commit {0}'.format(path.encode('utf-8')))
        elif self.vcs_type == 'hg':
            #_lock = self.r.lock()
            print '=' * 35
            print self.r.root
            print path
            print '=' * 35
            hg.add(self.ui, self.r, path.encode('utf-8'))
            hg.commit(
                self.ui,
                self.r,
                path.encode('utf-8'),
                message='commit {0}'.format(path))
            #_lock.release()

    def get_branches(self):
        """Gets a list of available branches in the repo"""
        if self.vcs_type == 'git':
            branches = self.r.get_refs().keys()
        elif self.vcs_type == 'hg':
            branches = self.r.branchmap().keys()
        return branches

    def get_tree(self, branch, path):
        if self.vcs_type == 'git':
            branch = branch or 'HEAD'
            # get the tree for the branch
            branches = self.r.get_refs().keys()
            if branch not in branches:
                branch = 'HEAD'
            if branch in branches:
                tree_id = self.r[branch].tree
                # get the objects in this tree
                objects = self.r.object_store.iter_tree_contents(tree_id)
                #get the paths of the objects
                l = [x.path for x in objects]
            else:
                l = ["Nothing has yet been done on your repo..."]
        elif self.vcs_type == 'hg':
            branch = branch or 'default'
            branches = self.r.branchmap().keys()
            try:
                if branch not in branches:
                    branch = self.r.branchmap().keys()[0]
                self.ui.pushbuffer()
                l = hg.locate(self.ui, self.r, branch=branch)
                l = self.ui.popbuffer().split('\n')
            except IndexError:
                branch = None
                l = ["Nothing has yet been done on your repo..."]
            #except:
                #s['branch'] = 'default'
        dico = {}
        for x in l:
            l2w(x, dico)
        hierarchy = dico[path]
        return branch, hierarchy

    def list_commits(self, branch):
        if self.vcs_type == 'git':
            branch = branch or 'HEAD'
            # using walker and a ref (branch)
            branches = self.r.get_refs()
            if branch not in branches:
                branch = 'HEAD'
            if branch in branches:
                w = self.r.get_walker([self.r.refs[branch]])
                #w = r.get_walker([r.refs['refs/heads/sqlite']])
                l = [x.commit for x in w]
            else:
                l = ["Nothing has yet been done on your repo..."]
        elif self.vcs_type == 'hg':
            branch = branch or 'default'
            branches = self.r.branchmap().keys()
            if branch not in branches:
                branch = 'default'
            #if s['branch'] not in branches:
            try:
                self.ui.pushbuffer()
                hg.log(self.ui, self.r, branch=[branch])
                l = self.ui.popbuffer().split('\n\n')
            except:
                branch = 'default'
                l = ["Nothing has yet been done on your repo..."]
        return branch, l

    def get_content(self, path, branch):
        content = ["Sorry no content"]
        if self.vcs_type == 'git':
            branch = branch or 'HEAD'
            # get the tree for the branch
            branches = self.r.get_refs()
            if branch not in branches:
                branch = 'HEAD'
            tree_id = self.r[branch].tree
            # get the objects in this tree
            objects = self.r.object_store.iter_tree_contents(tree_id)
            path_sha = [x.sha for x in objects if x.path == path]
            if len(path_sha) == 1:
                content = self.r.get_object(path_sha[0])
                content = content.as_raw_string().split('\n')
            else:
                content = ["sorry, could not find this file!"]
        elif self.vcs_type == 'hg':
            branch = branch or 'default'
            branches = self.r.branchmap().keys()
            if branch not in branches:
                branch = self.r.branchmap().keys()[0]
            _br = self.r[branch]
            self.ui.pushbuffer()
            hg.locate(self.ui, self.r, branch=branch)
            _file = self.ui.popbuffer().split('\n')
            if path in _file:
                content = _br.filectx(path).data().split('\n')
            else:
                content = ["sorry, could not find this file!"]
        return branch, content
