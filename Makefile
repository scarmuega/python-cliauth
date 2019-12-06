wheel:
	python3 setup.py sdist bdist_wheel

pypi-upload:
	twine upload dist/*

all: wheel pypi-upload