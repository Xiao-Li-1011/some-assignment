wordchains: wordchains.o stack.o
	gcc -o wordchains wordchains.o stack.o

wordchains.o : wordchains.c stack.h
	gcc -Wall -Werror -c wordchains.c

Graph.o : stack.c stack.h
	gcc -Wall -Werror -c stack.c

clean:
	rm -f wordchains wordchains.o stack.o core
	


