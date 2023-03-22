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
	
build:
	pyinstaller main.py *.py --onefile --icon assets/icon.png  -n PyMIPS

dependencies:
	@echo "********** Installing dependencies **********"
	@echo "********** Installing PyInstaller ***********"
	pip3 install pyinstaller
	@echo "********** Installing PyQt5 *****************"
	pip3 install PyQt5

clean:
	rm -rf dist/
	rm -rf build/
	rm *.spec
