g++ -std=c++14 -c -fPIC C/core.cpp C/gate.cpp C/utill.cpp
g++ -shared -O3 -o csim.so core.o gate.o utill.o
rm core.o gate.o utill.o
