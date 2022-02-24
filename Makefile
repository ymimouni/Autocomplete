help:
	@echo "Targets in Makefile:"
	@cat Makefile

init:
	pip install -r requirements.txt

dev:
	pip install -e .

test:
	pytest --tb=short

all: init dev test