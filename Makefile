deploy:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr	
	rm -fr *.egg *.egg-info/ dist/ build/ docs/_build/
	python3.6 setup.py sdist
	twine upload dist/*
