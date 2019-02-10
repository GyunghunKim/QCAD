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
	bool is_controlled;
	
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

	//Getters and Setters
	bool isControlled() {
		return is_controlled;
	}
	int getNumMatrix() {
		return num_matrix;
	}
	int getNumTarget() {
		return num_target;
	}
	int getNumControlled() {
		return num_controlled;
	}
	std::vector<int> getControls() {
		return controls;
	}
	std::vector<int> getTargets() {
		return targets;
	}
	field** getMatrix() {
		return matrix;
	}
};
