#pragma once 

#include <complex>
#include <string>
#include <vector>

#define PI 3.14159265359

using field = std::complex<double>;
using namespace std::complex_literals;

class Gate {
private:
	std::string name;
	
	int n;
	int num_matrix, num_target, num_controlled;
	bool isControlled;
	
	std::vector<int> controls;
	std::vector<int> targets;

	field** matrix;

public:
	Gate();
	Gate(const Gate &g);
	Gate(char* name, double matrix_real[], double matrix_imag[], bool is_controlled,
		int num_target, int targets[], int num_controlled, int controls[]);
	~Gate();

	void print();
};

void applyGate(Gate gate, field *state, int n);
void applySingleGate(std::string gate, int target, field *state, int n);
