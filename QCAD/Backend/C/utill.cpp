#include "utill.h"

#include <iostream>

void printBit(int n, int size, bool reverse) {
	for (int i = 0; i < size; i++) {
		std::cout << ((n >> (reverse ? i : size-i-1)) & 1);
	}
}
