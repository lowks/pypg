.PHONY: test

test:
	nosetests --verbose --with-cover --cover-erase --cover-package=pypg

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
