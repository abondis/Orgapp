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
remote_refs = client.fetch('test', r)
# refs from the remote
remote_refs.keys()
# set local repo's HEAD to be the same as remote's HEAD
r["HEAD"] = remote_refs["HEAD"]
# set local repo's bootstrap branch
# to be the same as remote's bootstrap branch
r["refs/heads/master"] = remote_refs["refs/heads/master"]

# git push (local to ssh)
src = "git+ssh://git@redmine.kerunix.com/test"
dest = "/tmp/dest-repo"
os.mkdir(dest)
dest_repo = Repo.init(dest)
client, host = get_transport_and_path(src)

print host
client.send_pack(
    host,
    r.object_store.determine_wants_all,
    r.object_store.generate_pack_contents)
