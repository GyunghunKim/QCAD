#pragma once 

#include <complex>
#include <string>
#include <vector>

#define PI 3.14159265359

using field = std::complex<double>;
using namespace std::complex_literals;

class Gate {
public:
	bool isControlled;
	std::string name;
	std::vector<int> controls;
	std::vector<int> targets;

	Gate();
	void print();
};

void applyGate(Gate gate, field *state, int n);
void applySingleGate(std::string gate, int target, field *state, int n);
