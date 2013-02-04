start: init
	cd src; ../venv/bin/python webui.py

init: venv
	git submodule update --init

venv: venv/bin/activate

venv/bin/activate: src/requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur src/requirements.txt
	touch venv/bin/activate
