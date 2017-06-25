
dist: backend_dist frontend_dist
	test -d dist || mkdir dist; rm -rf dist/*
	cp Flask-Server/dist/Timeswitch-*.tar.gz dist/
	cp -r Client/build dist/frontend

test:
	$(MAKE) -C Flask-Server test

frontend_run_dev:
	$(MAKE) -C Client run_dev

frontend_dist:
	$(MAKE) -C Client dist

backend_run_dev:
	$(MAKE) -C Flask-Server run_dev

backend_run_dev_static:
	$(MAKE) -C Flask-Server run_dev_static

backend_dist:
	$(MAKE) -C Flask-Server dist

.PHONY : backend_run_dev backend_dist frontend_dist frontend_run_dev \
	test
