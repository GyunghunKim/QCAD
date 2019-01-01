SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd )

g++ -std=c++14 -c -Wall -fPIC $SCRIPTPATH/C/*.cpp
g++ -shared -O3 *.o -o csim.so
mv csim.so $SCRIPTPATH/csim.so
rm *.o
