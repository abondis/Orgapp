Versioning
==========

Need to:
--------

* be able to version wiki pages
* from command line using git
* from webui (using dulwich)
* pure python library

Basics
------

	from dulwich import repo
	r = repo.Repo('path/to/repo')

Edit
----
	
	f = open('a/file', 'wb')
	f.write("= test =\n\n* test\n")
	f.close()

Stage
-----

	r.stage("a/file")

Commit
------

	r.do_commit(message="commit message")

Push
----
TO DO
  
  