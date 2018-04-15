.DEFAULT_GOAL := build

clean:
	rm -rf code.zip suds*

install:
	pip install -r requirements.txt -t `pwd`

build: clean install
	zip -qyr code.zip . -x@.lambdaignore