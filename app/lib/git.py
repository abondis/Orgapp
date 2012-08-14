#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import os
from dulwich.client import get_transport_and_path, SSHGitClient
from dulwich.repo import Repo


# git pull, uses ssh keys and $PATH/ssh
dest = "/tmp/test"
os.mkdir(dest)
# local repository
r = Repo.init(dest)
# create client object
client = SSHGitClient('redmine.kerunix.com', username='git')
# fetch repo from source repo
remote_refs = client.fetch('orgapp', r)
# refs from the remote
remote_refs.keys()
# set local repo's HEAD to be the same as remote's HEAD
r["HEAD"] = remote_refs["HEAD"]
# set local repo's bootstrap branch
# to be the same as remote's bootstrap branch
r["refs/heads/bootstrap"] = remote_refs["refs/heads/bootstrap"]

# git push (local to local)
src = "/tmp/src-repo"
dest = "/tmp/dest-repo"
os.mkdir(src)
os.mkdir(dest)
src_repo = Repo.init(src)
dest_repo = Repo.init(dest)
client, host = get_transport_and_path("/tmp/blah/")

client.send_pack(
    '/tmp/blah',
    r.object_store.determine_wants_all(),
    r.object_store.generate_pack_contents())
