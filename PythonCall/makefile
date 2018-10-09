#sample makefile test1

CC = gcc
SRCS = main.cpp
EXEC = test

INCLUDES = -I/usr/include/python2.6/  
LINKS   = -L/usr/lib/ -lpython2.6
all:
	$(CC) -lstdc++  -std=c++11  $(SRCS) -o $(EXEC) $(INCLUDES) $(LINKS)

clean:
	rm -rf $(EXEC)
	rm -rf *.pyc

