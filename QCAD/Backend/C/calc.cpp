#include "calc.h"

int bitToInt(int n, int* mask) {
	int res = 0;

	for (int i = 0; i < n; i++)
		res += mask[i] * (1 << i);

	return res;
}

//(SubFunction) A = MA
void matrixMultiplicate(int n, field** m, field* a) {
	field* res = new field[n]();

	for (int i = 0; i < n; i++)
		for (int j = 0; j < n; j++)
			res[i] += m[i][j] * a[j];

	for (int i = 0; i < n; i++)
		a[i] = res[i];
}

void subGetPoints(int n, std::vector<int> &points, int* mask, Gate g, int ind) {
	if (ind == g.getNumTarget()) {
		points.push_back(bitToInt(n, mask));		
		return;
	}
	mask[g.getTargets()[g.getNumTarget()-ind-1]] = 0;
	subGetPoints(n, points, mask, g, ind+1);
	mask[g.getTargets()[g.getNumTarget()-ind-1]] = 1;
	subGetPoints(n, points, mask, g, ind+1);
	mask[g.getTargets()[g.getNumTarget()-ind-1]] = -1;
}

void subGateMatrixMultiplicate(int n, std::vector<int> points, field* state, Gate g) {

	field* temp = new field[points.size()];

	for (unsigned int i = 0; i < points.size(); i++)
		temp[i] = state[points[i]];

	matrixMultiplicate(points.size(), g.getMatrix(), temp);

	for (unsigned int i = 0; i < points.size(); i++)
		state[points[i]] = temp[i];
}

//(SubFunction) get Mask
void subGetMask(int n, int* mask, int ind, field* state, Gate g) {
	if (ind >= n) {
		std::vector<int> points;

		subGetPoints(n, points, mask, g, 0);

		subGateMatrixMultiplicate(n, points, state, g);
	
		return;
	}	

	while(mask[ind] == -1 || mask[ind] == 1) {
		ind++;
		if (ind >= n)
			subGetMask(n, mask, ind, state, g);
	}
	if (ind < n) {
		subGetMask(n, mask, ind+1, state, g);
		mask[ind] = 1;
		subGetMask(n, mask, ind+1, state, g);
		mask[ind] = 0;
	}
}

void applyGate(int n, field* state, Gate g) {
	//단일 게이트의 경우 빨리 처리된다.
/*	if (g.isControlled() == false && g.getNumTarget() == 1) {
		int target = g.getTargets()[0];
		
		int size1 = 1 << target;
		int size2 = 1 << (n-target-1);

		field** gate = g.getMatrix();

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
*/	
	//mask는 비트를 나타낸다.
	//값이 -1이면 행렬 연산을 가해야 한다. 탐색을 통해 만들어낸다.	
	int* mask = new int[n]();
	
	for (int i: g.getTargets()) {
		mask[i] = -1;
	}
	
	//Controlled Gate인 경우 어떤 비트들은 반드시 1이어야 한다.
	if (g.isControlled()) {
		for (int i: g.getControls()) {
			mask[i] = 1;
		}
	}

	subGetMask(n, mask, 0, state, g);
}
