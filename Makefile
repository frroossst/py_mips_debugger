.PHONY: *

OUTPUT = output
PYTHONFILE = main.py
PYTHONLIBVER = python3.10
CFILE=main.c

help:
	@echo "make help"
	@echo "    Show this message"
	@echo "make build"
	@echo "    Build the binary file"
	@echo "make run"
	@echo "    Run the binary file"
	@echo "make clean"
	@echo "    Remove the binary file"
	
build:
	cython $(PYTHONFILE) --embed
	gcc -Os -I/usr/include/$(PYTHONLIBVER) $(python3-config --includes) main.c -o output $(python3-config --ldflags) -l$(PYTHONLIBVER)

run:
	./output

dependencies:
	@echo "********** Installing dependencies **********"
	@echo "********** Installing Cython ****************"
	pip3 install cython3
	@echo "********** Installing PyQt5 *****************"
	pip3 install PyQt5

clean:
	rm -f output
	rm -f *.c
	rm -f *.o
