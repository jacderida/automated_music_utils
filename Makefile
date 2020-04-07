.ONESHELL:
unit-tests:
	source env/bin/activate
	nosetests tests/unit

.ONESHELL:
integration-tests:
	source env/bin/activate
	nosetests tests/integration

.ONESHELL:
tests: unit-tests integration-tests

.ONESHELL:
unit-tests-with-coverage:
	source env/bin/activate
	rm -f .coverage
	rm -rf htmlcov
	nosetests tests/unit --with-coverage

.ONESHELL:
integration-tests-with-coverage:
	source env/bin/activate
	rm -f .coverage
	rm -rf htmlcov
	nosetests tests/unit --with-coverage
