.PHONY: all help run test unittests

all: help

help:
	 @echo "Usage:"
	 @echo " make run - run the app"
	 @echo " make test - run tests locally"
	 @echo " make docker/build - run docker-compose up --build"
	 @echo " make docker/run - run docker-compose up -d"
	 @echo " make black - Runs black library on all of the modules in src folder"
	 @echo " make lint - Runs pylint to check the code quality"

run:
	 python3 src/main.py

docker/build:
	 docker-compose up --build

docker/run:
	 docker-compose up -d

test: requirements
	 @pytest  

requirements:
	 @pip3 install -r requirements.txt

black:
	@black src/

lint:
	@pylint src/