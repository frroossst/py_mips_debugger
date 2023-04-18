.PHONY: *

help:
	@echo "Usage: make [OPTIONS]\n"
	@echo "Options:\n"
	@echo "help"
	@echo "    Show this message"
	@echo "build"
	@echo "    Build the binary file"
	@echo "dependencies"
	@echo "    Install the dependencies"
	@echo "docs"
	@echo "    Generate the documentation"
	@echo "clean"
	@echo "    Remove the build files"
	
build:
	@echo "**********************************************"
	@echo "********** Building the binary file **********"
	@echo "**********************************************"
	pyinstaller main.py *.py --onefile --icon assets/icon.png  -n PyMIPS
	@echo "******************** End ********************"

dependencies:
	@echo "**********************************************"
	@echo "********** Installing dependencies **********"
	@echo "**********************************************"
	@echo "********** Installing PyInstaller ***********"
	pip3 install pyinstaller
	@echo "********** Installing PyQt5 *****************"
	pip3 install PyQt5
	@echo "******************** End ********************"

docs:
	@echo "**********************************************"
	@echo "********** Generating documentation **********"
	@echo "**********************************************"
	mdbook build docs/
	mv ./docs/src/ .
	rm -rf ./docs
	mkdir docs/
	mv src/ docs/
	mdbook build docs/
	mv -f docs/book/* docs/	
	@echo "******************** End ********************"

clean:
	@echo "**********************************************"
	@echo "********** Removing build files **************"
	@echo "**********************************************"
	rm -rf dist/
	rm -rf build/
	rm *.spec
	@echo "******************** End ********************"

