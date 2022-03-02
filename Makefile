help:
	@echo set target to run "make" command
	@echo target: install, update, lint, format, clean

install:
	@echo -------------------- install packages ----------------------------------------------------
	@poetry install

update:
	@echo -------------------- update packages -----------------------------------------------------
	@poetry update

lint:
	@echo -------------------- run pflake8 to check grammar ----------------------------------------
	@poetry run pflake8 --statistics .
	@echo -------------------- run isort to check import statement ---------------------------------
	@poetry run isort --check .
	@echo -------------------- run mypy to check type ----------------------------------------------
	@poetry run mypy .

format:
	@echo -------------------- run isort to format import statement --------------------------------
	@poetry run isort .

clean:
	@echo -------------------- clean package -------------------------------------------------------
	@rmdir /s /q .mypy_cache .pytest_cache .venv
