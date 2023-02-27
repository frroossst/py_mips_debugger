.PHONY: *

OUTPUT = output
PYTHONFILE = main.py
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
	gcc -Os -I /usr/include/python3.3m -o $(OUTPUT) $(CFILE) -lpython3.3m -lpthread -lm -lutil -ldl

run:
	./output_bin_file

dependencies:
	pip3 install cython
	pip3 install PyQt5

clean:
	rm -f output_bin_file
	rm -f *.c

