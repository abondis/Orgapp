
running
-------

next
----
* styling: [pyScss](https://github.com/Kronuz/pyScss/) and [semantic](http://semantic.gs/)
* tasks: tasks/<taskid> to view a task details
* tasks: details comme une page de wiki
* wiki: list commits
* wiki: rollback (or diff and keep/commit prefered version)
* tasks api with bottle
* tasks UI with bottle

backlog
-------
* get paths out of the code (use os.path.getcwd)
* cache a wiki  (multiple levels, files ie: images)
* UI: switch branch
* authentication
* multi-users

done
----
* add/move/status for tasks
* cache a wiki folder (1 level, only *.something -> html)
* plug bottle to show wiki and tasks
* render wiki pages with a markup (markdown)
* cache a wiki folder (1 level, non html files are routed by bottle)
* wiki: edit -> doc.py save(path, newcontent)
* wiki: commit -> doc.py commit(path)
* UI: wiki load file in textarea
* UI: wiki save file
* UI: wiki commit
* wiki: refresh cache
* cache wiki with cp -R + render -> md5 between old and new, cache only if different, if not a rendered type copy the raw content, else remove .ext
* BUG: content gets "   " added at the beginning -> was in the template

  
  