.PHONY: format publish

check-code:
	pycodestyle begoneads --max-line-length=120

format: begoneads/**/*.py
	autopep8 --in-place begoneads/**/*.py

publish-pypi:
	rm -rf dist/*
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

publish: publish-pypi
