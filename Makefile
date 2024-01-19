init:
	python -m pip install '.[dev]'

bundle:
	make init
	rm -rf dist
	python -m build --sdist

publish:
	make bundle
	python -m twine upload --repository pypi dist/*

test:
	make init
	rm -f .coverage
	rm -rf htmlcov
	python -m pytest --cov=src --cov-report html --cov-report term

format:
	make init
	python -m black .
	python -m isort .