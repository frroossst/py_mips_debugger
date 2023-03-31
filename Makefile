.PHONY: *

help:
	@echo "********** Makefile Help **********"
	@echo "how to use this Makefile:"
	@echo "1. make dependencies"
	@echo "2. make build"
	@echo "***********************************"
	@echo "make help"
	@echo "    Show this message"
	@echo "make build"
	@echo "    Build the binary file"
	@echo "make dependencies"
	@echo "    Install the dependencies"
	@echo "make clean"
	@echo "    Remove the build files"
	@echo "make docs"
	@echo "    Generate the documentation"
	
build:
	pyinstaller main.py *.py --onefile --icon assets/icon.png  -n PyMIPS

dependencies:
	@echo "********** Installing dependencies **********"
	@echo "********** Installing PyInstaller ***********"
	pip3 install pyinstaller
	@echo "********** Installing PyQt5 *****************"
	pip3 install PyQt5

docs:
	@echo "********** Generating documentation **********"
	mdbook build docs/
	mv -f docs/book/* docs/	

clean:
	rm -rf dist/
	rm -rf build/
	rm *.spec
	rm -rf ./docs/FontAwesome
	rm -rf ./docs/css
	rm -rf ./docs/fonts

