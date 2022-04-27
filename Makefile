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

.PHONY: menace_train
menace_train:
	poetry run python ticTacToe/learning.py

.PHONY: menace_play
menace_play:
	poetry run python ticTacToe/menace.py