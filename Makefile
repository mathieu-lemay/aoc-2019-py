.PHONY: unittests coverage deps clean

unittests: deps
	poetry run python -m unittest discover tests

coverage: deps
	poetry run coverage run -m unittest discover tests
	poetry run coverage report

deps: .make.poetry

clean:
	rm .make.*

.make.poetry: pyproject.toml poetry.lock
	poetry install
	touch .make.poetry

# vim: noet
