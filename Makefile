.PHONY: format publish

format: *.py
	autopep8 --in-place *.py

publish-pypi:
	rm -rf dist/*
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

publish: publish-pypi
