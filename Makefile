.PHONY: build publish-test install lint test clean

build:
	rm -rf dist/
	rm -rf build/
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

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf .pytest_cache/
