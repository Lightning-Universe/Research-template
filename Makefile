coverage:  ## Run tests with coverage
		coverage erase
		coverage run -m pytest
		coverage report -m
		coverage xml

clean:
	rm -rf dist
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	rm -f .coverage

style:
	black .
	isort --profile black .

push:
	git push && git push --tags

sync-template:
	git fetch --all
	git merge template/main

release-dev:
	lightning run app app.py --cloud --name 'Research Poster Dev'

release-prod:
	lightning run app app.py --cloud --name 'Research Poster'

release-clip_demo:
	lightning run app app.py --cloud --name 'Unsplash Image Search: Clip Demo'
