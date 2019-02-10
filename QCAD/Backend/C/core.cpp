#include "gate.h"
#include "calc.h"

#include <vector>
#include <iostream>
#include <ctime>

int num_qubit;
std::vector<Gate> gates;
field *state;

extern "C" {
	void setNumQubit(int n);
	void resetQC();
	void addGate(char* name, double matrix_real[], double matrix_imag[], bool is_controlled,
		int num_target, int targets[], int num_controlled, int controls[]);
	void printQCStatus();
	double* run(double state_real[], double state_imag[]);
}

void setNumQubit(int n) {
	num_qubit = n;
	state = new field[1<<num_qubit]();
} 

void resetQC() {
	num_qubit = 0;
	gates.clear();
	delete []state;
}

void addGate(char* name, double matrix_real[], double matrix_imag[], bool is_controlled,
		int num_target, int targets[], int num_controlled, int controls[]) {

	Gate g(name, matrix_real, matrix_imag, is_controlled, num_target,
			targets, num_controlled, controls);

	gates.push_back(g);
}

void printQCStatus() {
	std::cout << "Number of Qubits: " << num_qubit << std::endl;
	for (auto gate: gates) {
		gate.print();
	}
}

double* run(double state_real[], double state_imag[]) {
	for (int i = 0; i < 1<<num_qubit; i++)
		state[i] = field(state_real[i], state_imag[i]);
	
	std::clock_t begin = std::clock();
	
	for (auto &gate: gates)
		applyGate(num_qubit, state, gate);

	std::clock_t end = std::clock();

	std::cout << "Elapsed Time: " << (double)(end - begin)/CLOCKS_PER_SEC << std::endl << std::endl;

	double* res = new double[(1<<num_qubit) * 2];

	for (int i = 0; i < 1<<num_qubit; i++) {
		res[i] = state[i].real();
		res[(1<<num_qubit) + i] = state[i].imag();
	}

	return res; 
}
