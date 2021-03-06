TEST_PATH=./tests

.PHONY: requirements
requirements:
	poetry install

.PHONY: test
test: requirements
	poetry run pytest -vv --color=yes $(TEST_ONLY)

.PHONY: format
format: requirements_tools
	poetry run black .

.PHONY: menace
menace:
	poetry run python ticTacToe/menace.py

.PHONY: minmax
minmax:
	poetry run python ticTacToe/minmax.py