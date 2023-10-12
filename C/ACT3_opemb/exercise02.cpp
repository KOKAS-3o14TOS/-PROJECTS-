#include <iostream>
#include <iomanip>
#include <chrono>
#include <cmath>
#include <cstring>
#include <omp.h>
#include "utils.h"
#define MAX 5000000

using namespace std;
using namespace std::chrono;

bool es_primo(int n){
	if (n<2) return false;
	for(int i=2;i<=sqrt(n);i++){
		if (n%i==0) return false;
	}
	return true;
}

void sumar(int *array,int &suma,int max){
    #pragma omp parallel for shared(array, suma, max)
    for(int i=0;i<max;i++){
		if (es_primo(array[i])){
			suma+=i;
		}
	}
}

int main(int argc, char* argv[]) {
	int *array;
	int suma = 0;
	////////////////
	high_resolution_clock::time_point start, end;
	double timeElapsed;
	////////////////
	array = new int[MAX];
    fill_array(array,MAX);
	display_array("array", array);
	cout << "Starting...\n";
	timeElapsed = 0;//////////////////////////////
	for (int j = 0; j < N; j++) {
		start = high_resolution_clock::now();/////////////////////////
		sumar(array,suma,MAX);
		end = high_resolution_clock::now();///////////////////////////
		timeElapsed += duration<double, std::milli>(end - start).count();////////////////////////////
	}
	cout<<suma<<"\n";
	cout << "avg time = " << fixed << setprecision(3) << (timeElapsed / N) <<  " ms\n";/////////////////////////////
	delete [] array;
	return 0;
}
