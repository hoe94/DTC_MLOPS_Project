code_checks:
	black .
	isort .

unit_test:
	pytest unit_test/