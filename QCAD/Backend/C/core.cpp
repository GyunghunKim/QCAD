#include "gate.h"
#include "utill.h"

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
	//TODO: Delete this!
	for (int i = 0; i < 1<<num_qubit; i++)
		state[i] = field(state_real[i], state_imag[i]);
/*
	double *prob = new double[(int)std::exp2(num_qubit)]();
	
	std::clock_t begin = std::clock();
	for (int i = 0; i < gates.size(); i++) {
		if (gates[i].targets.size() == 1)
			applySingleGate(gates[i].name, gates[i].targets[0], state, num_qubit);
	}

	for (int i = 0; i < std::exp2(num_qubit); i++)
		prob[i] = std::abs(state[i]);
	std::clock_t end = std::clock();

	for (int i = 0; i < std::exp2(num_qubit); i++)
		if (prob[i] != 0) {
			printBit(i, num_qubit, true);
			std::cout << ": " << prob[i]*prob[i] << std::endl;
		}

	std::cout << "Elapsed Time: " << (double)(end - begin)/CLOCKS_PER_SEC << std::endl << std::endl;
*/

	double* res = new double[(1<<num_qubit) * 2];

	for (int i = 0; i < 1<<num_qubit; i++) {
		res[i] = state[i].real();
		res[(1<<num_qubit) + i] = state[i].imag();
	}

	return res; 
}
