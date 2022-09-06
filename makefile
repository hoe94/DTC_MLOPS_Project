code_checks:
	black .
	isort .

unit_test:
	pytest unit_testing/

docker_image_build: code_checks unit_test
	docker build -t mlops-project-credit-score-prediction:v1 .

integration_test: docker_image_build
	bash integration_test/run.sh