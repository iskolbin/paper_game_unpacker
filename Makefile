run:
	mkdir -p badges
	./venv/bin/python badges.py	

venv:
	mkdir -p venv
	python -m venv venv/
	./venv/bin/pip install pillow
	./venv/bin/pip install pdf2image
