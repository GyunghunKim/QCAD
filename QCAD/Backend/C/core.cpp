#include "gate.h"

#include <vector>
#include <iostream>

int num_qubit;
std::vector<Gate> gates;
field *state;

extern "C" void setNumQubit(int n) {
	num_qubit = n;
	state = new field[(int)std::exp2(num_qubit)];
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
	std::cout << "Number of Qubits : " << num_qubit << std::endl;
	for (int i = 0; i < gates.size(); i++) {
		std::cout << "Gate Name : " << gates[i].name << ", Targets : ";
		for (int j = 0; j < gates[i].targets.size(); j++)
			std::cout << gates[i].targets[j] << " ";
		std::cout << std::endl;	
	}
}
