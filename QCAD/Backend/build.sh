g++ -std=c++14 -c -fPIC C/core.cpp C/gate.cpp
g++ -shared -O3 -o csim.so core.o gate.o
rm core.o gate.o
