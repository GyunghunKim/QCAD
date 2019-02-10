#include "gate.h"

#include <iostream>

Gate::Gate() {
}

Gate::Gate(const Gate &g) {
	this->name = g.name;
	this->n = g.n;
	this->num_matrix = g.num_matrix;
	this->num_controlled = g.num_controlled;
	this->num_target = g.num_target;
	this->is_controlled = g.is_controlled;
	this->targets = g.targets;
	this->controls = g.controls;

	this->matrix = new field*[num_matrix];
	for (int i = 0; i < num_matrix; i++) {
		this->matrix[i] = new field[num_matrix];
		for (int j = 0; j < num_matrix; j++) {
			this->matrix[i][j] = g.matrix[i][j];
		}
	}
}

Gate::Gate(char* name, double matrix_real[], double matrix_imag[], bool is_controlled,
		int num_target, int targets[], int num_controlled, int controls[]) {

	this->name = name;
	this->n = num_target + num_controlled;
	this->num_matrix = 1 << num_target;
	this->num_target = num_target;
	this->num_controlled = num_controlled;
	this->is_controlled = is_controlled;

	for (int i = 0; i < num_target; i++)
		this->targets.push_back(targets[i]);
	
	if (is_controlled) {
		for (int i = 0; i < num_controlled; i++)
			this->controls.push_back(controls[i]);
	}

	this->matrix = new field*[num_matrix];
	for (int i = 0; i < num_matrix; i++) {
		this->matrix[i] = new field[num_matrix];
		for (int j = 0; j < num_matrix; j++)
			this->matrix[i][j] = field(matrix_real[i * num_matrix + j],
					matrix_imag[i * num_matrix + j]);
	}
}

Gate::~Gate() {
	for (int i = 0; i < num_matrix; i++)
		delete[] matrix[i];
	delete[] matrix;	
}

void Gate::print() {
	std::cout << "----------------------" << std::endl
		<< "Name		: " << name << std::endl
		<< "IsControlled	: " << is_controlled << std::endl;

	std::cout << "Controls	: ";
	for (int i = 0; i < num_controlled; i++)
		std::cout << controls[i] << " ";
	std::cout << std::endl << "Targets		: ";
	for (int i = 0; i < num_target; i++)
		std::cout << targets[i] << " ";
	std::cout << std::endl << "Matrix" << std::endl;
	for (int i = 0; i < num_matrix; i++) {
		for (int j = 0; j < num_matrix; j++) {
			std::cout << matrix[i][j] << " ";
		}
		std::cout << std::endl;
	} 
	std::cout << "----------------------" << std::endl;
}

//void applySingleGate(std::string gate_name, int target, field *state, int n) {
//	int size1 = 1 << target;
//	int size2 = 1 << (n-target-1);
//
//	field (*gate)[2] = gateParser(gate_name);
//
//	for (int i = 0 ; i < size2; i++) {
//		for (int j = 0; j < size1; j++) {
//			int a = (i << (target+1)) + j;
//			int b = a + (1 << target);
//
//			field imsi = state[a];
//			state[a] = gate[0][0] * imsi + gate[0][1] * state[b];
//			state[b] = gate[1][0] * imsi + gate[1][1] * state[b];		
//		}
//	}	
//}
