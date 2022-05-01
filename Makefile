.PHONY: build publish-test install lint test

build:
	python -m build --sdist
	python -m build --wheel
	twine check dist/*

publish-test:
	twine upload --repository testpypi dist/*

install:
	pip install -r requirements.txt
	pip install -e .

lint:
	pylint --version
	pylint ech_datastructures/

test:
	pytest
