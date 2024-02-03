.PHONY: local local-install local-uninstall update clean check

local: local-uninstall local-install
	
local-uninstall:
	python -m pip uninstall -y github_release_downloader

local-install:
	python -m pip install .

update:
	@rm -f requirements.txt
	./setup

clean:
	@rm -rf build github_release_downloader.egg-info
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

check:
	@python setup.py check