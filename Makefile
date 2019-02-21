.PHONY: format

format: *.py
	autopep8 --in-place *.py
