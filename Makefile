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
run_rl:
	poetry run python menace/learning.py