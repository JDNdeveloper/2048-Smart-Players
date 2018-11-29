all: libExpectiMaxPlayer.so ;

clean:
	rm -f libExpectiMaxPlayer.so ExpectiMaxPlayer.o

libExpectiMaxPlayer.so: ExpectiMaxPlayer.o
	g++ -shared -Wl,-soname,libExpectiMaxPlayer.so -o libExpectiMaxPlayer.so \
		ExpectiMaxPlayer.o

ExpectiMaxPlayer.o: ExpectiMaxPlayer.cpp ExpectiMaxPlayer.h
	g++ -c -fPIC ExpectiMaxPlayer.cpp -o ExpectiMaxPlayer.o
