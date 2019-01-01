#include "gate.h"

field H[2][2] = {{sqrt(0.5), sqrt(0.5)}, {sqrt(0.5), -sqrt(0.5)}}; 
field X[2][2] = {{0, 1}, {1, 0}}; 
field Y[2][2] = {{0, 1i}, {-1i, 0}};
field Z[2][2] = {{1, 0}, {0, -1}}; 
field I[2][2] = {{1, 0}, {0, 1}};
field T[2][2] = {{1, 0}, {0, sqrt(0.5)+sqrt(0.5)*1i}};
field S[2][2] = {{1, 0}, {0, 1i}};

field (*gateParser(std::string gate_name))[2] {
	if (gate_name.compare("H") == 0)
		return H;
	if (gate_name.compare("X") == 0)
		return X;
	if (gate_name.compare("Y") == 0)
		return Y;
	if (gate_name.compare("Z") == 0)
		return Z;
	if (gate_name.compare("I") == 0)
		return I;
	if (gate_name.compare("T") == 0)
		return T;
	if (gate_name.compare("S") == 0)
		return S;
	return NULL;
}

void applyGate(Gate gate, field *state, int n) {
	if (gate.targets.size() == 1)
		applySingleGate(gate.name, gate.targets[0], state, n);
}

void applySingleGate(std::string gate_name, int target, field *state, int n) {
	int size1 = 1 << target;
	int size2 = 1 << (n-target-1);

	field (*gate)[2] = gateParser(gate_name);

	for (int i = 0 ; i < size2; i++) {
		for (int j = 0; j < size1; j++) {
			int a = (i << (target+1)) + j;
			int b = a + (1 << target);

			field imsi = state[a];
			state[a] = gate[0][0] * imsi + gate[0][1] * state[b];
			state[b] = gate[1][0] * imsi + gate[1][1] * state[b];		
		}
	}	
}
