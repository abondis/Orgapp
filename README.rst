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

.. warning:: **Orgapp is still beeing in development. Basic tests have been done, but not yet**
  **in production. Use at your own risks and after having done a lot of tests :)**

Get Orgapp
^^^^^^^^^^

* clone the repository to your desired path

::

  git clone git@github.com:abondis/Orgapp.git

* and enter it

::

  cd Orgapp

* quickstart

::

  make start

Prepare the environment
^^^^^^^^^^^^^^^^^^^^^^^

* initialize the required submodules (only twitter-bootstrap)

::

  git submodule update --init

* enter the src folder

::

  cd src

* and initialize a python virtualenv (http://pypi.python.org/pypi/virtualenv)

::

  virtualenv env
  . env/bin/activate

* install the python dependencies

::

  pip install -r requirements.txt


Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

* configuration is done in two times

  1. configure the app by itself (where to find the repositories, where to cache
     the rendering, where to store the database)

  2. setup authorized users with bottle-cork

Configure the app
~~~~~~~~~~~~~~~~~

* orgapp will read the file config-\*.ini in the config/ folder
* it will use the first file it finds in the following

  1. config-dev.ini
  2. config-stage.ini
  3. config-prod.ini

* they have 3 sections:

  * doc: specify where is the repository's documentation (path relative to the
    repository's root)
  * tasks: full path to the tasks database
  * repos: full paths to the git and hg repositories


configure users
~~~~~~~~~~~~~~~

* needed to grant access to the edit functions of Orgapp

::

  python config/create_cork_users.py

Start Orgapp UI
~~~~~~~~~~~~~~~

* Orgapp gives an interface to handle tasks and view projects. For that you
  need to start its web interface, still from the src/ folder

::

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
* doc :)
* unittest
* cli

Authors
-------

* Aurélien Bondis
* Pierre Paul Lefebvre
