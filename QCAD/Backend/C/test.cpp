#include <iostream>
#include <complex>
#include <cmath>
#include <chrono>

using field = std::complex<float>;

using namespace std::complex_literals;

field H[2][2] = {{sqrt(0.5), sqrt(0.5)}, {sqrt(0.5), -sqrt(0.5)}};
field X[2][2] = {{1, 0}, {0, -1}};

void print_all(field state[], int n) {
	for (int i = 0; i < 1 << n; i++)
		std::cout << state[i] << std::endl;
}

void gate1(field gate[][2], int target, field state[], int n) {
	int size1 = 1 << target;
	int size2 = 1 << (n-target-1);

	for (int i = 0; i < size2; i++) {
		for (int j = 0; j < size1; j++) {
			int a = (i << (target+1)) + j;
			int b = a + (1 << target);
		
			field imsi = state[a];	
			state[a] = gate[0][0] * imsi + gate[0][1] * state[b];
			state[b] = gate[1][0] * imsi + gate[1][1] * state[b];			
		}
	}	
}

int main(void) {
	int N = 23;
	int SIZE = 1 << N;

	std::cout << SIZE << std::endl;
	
	field *state = new field[SIZE];
	state[0] = 1;

	using namespace std::chrono;

	high_resolution_clock::time_point t1 = high_resolution_clock::now();

	for (int i = 0; i < 100; i++)
		gate1(H, i % N, state, N);

	high_resolution_clock::time_point t2 = high_resolution_clock::now();

	auto duration = duration_cast<microseconds>( t2 - t1 ).count();

	std::cout << (float)duration/1000000 << std::endl;	

	std::cout << state[0];

	delete []state;

	return 0;
}
