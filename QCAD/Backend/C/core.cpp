#include "gate.h"
#include "utill.h"

#include <vector>
#include <iostream>

int num_qubit;
std::vector<Gate> gates;
field *state;

extern "C" void setNumQubit(int n) {
	num_qubit = n;
	state = new field[(int)std::exp2(num_qubit)]();
} 

extern "C" void resetQC() {
	num_qubit = 0;
	gates.clear();
	delete state;
}

extern "C" void addGate(char* name, int targets[], int num_target) {
	Gate g;

	g.name = name;
	for (int i = 0; i < num_target; i++)
		g.targets.push_back(targets[i]);
	
	gates.push_back(g);
}

extern "C" void printQCStatus() {
	std::cout << "Number of Qubits: " << num_qubit << std::endl;
	for (int i = 0; i < gates.size(); i++) {
		std::cout << "Gate: " << gates[i].name << ", Targets: ";
		for (int j = 0; j < gates[i].targets.size(); j++)
			std::cout << gates[i].targets[j] << " ";
		std::cout << std::endl;	
	}
}

//TODO: 12/30 Multi qubit gate (CX)에 대해 작동하도록 수정되어야 함.
//TODO: 12/30 출력 방식 정하고 완성해야 함.
extern "C" void run() {
	//TODO: Delete this!
	state[0] = 1;

	double *prob = new double[(int)std::exp2(num_qubit)]();
	
	for (int i = 0; i < gates.size(); i++) {
		applySingleGate(gates[i].name, gates[i].targets[0], state, num_qubit);
	}

	for (int i = 0; i < std::exp2(num_qubit); i++)
		prob[i] = std::abs(state[i]);

	for (int i = 0; i < std::exp2(num_qubit); i++)
		if (prob[i] != 0) {
			printBit(i, num_qubit, true);
			std::cout << ": " << prob[i]*prob[i] << std::endl;
		}
}
