Android
=======

Python
------

* orgapp uses pure python and standard libs only
* should work with sl4a

SSH
---

* using binaries because pycrypto is not pure python and fabric's SSH
  lib stil still depends on it
* install rsync4android and their binaries
* set $PATH to /data/data/eu.kowalczuk.rsync4android/files

Git
---

* should not be needed as we are using dulwich
