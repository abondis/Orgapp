Orgapp
======

Orgapp is a simple portable project management.
The goal is to have an app that can be used offline as well as online.

Tasks are created for projects, but they are prioritized relatively to each
other.

A project documentation is (for now, only) md files, tracked inside the repo.

Content of the projects tasks will (soon) be stored as part of the project to.

Repos can be git or mercurial repos, if they are not created previous to
running the webui, they will be initialized.

Getting started
---------------

.. WARNING::
  Orgapp is still beeing in development. Basic tests have been done, but not yet
  in production. Use at your own risks and after having done a lot of tests :)

* prepare

  git submodule update --init
  cd src
  virtualenv env
  . env/bin/activate
  pip install -r requirements.txt

* configure

  cp config/config-multiprojects-example.ini config/config-dev.ini

* configure users, used by bottle-cork, needs pycrypto

  python config/create_cork_users.py

* run

  python webui.py

* access to http://localhost:8080 , user: admin, password: test (cf
  create_cork_users)

More to come
------------

* sync
* how to install on android
* tasks in files
* push/pull
* permit different markups
* fixes :)
