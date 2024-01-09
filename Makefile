init:
	python -m pip install '.[dev]'

build:
	make init
	rm -rf dist
	python -m build --sdist

publish:
	make build
	python -m twine upload --repository pypi dist/*

test:
	make init
	rm -f .coverage
	rm -rf htmlcov
	python -m pytest --cov=src --cov-report html --cov-report term

