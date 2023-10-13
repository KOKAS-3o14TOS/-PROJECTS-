/*
Desarrolla una función que regresa la suma de todos los números primos que hay entre 1 y 5,000,000 (cinco millones).

Jorge Martínez Lopez A01704518
Gaddiel Lara Roldán A01704231

*/

#include <iostream>
#include <iomanip>
#include <chrono>
#include <omp.h>
#include <cmath>
#include "utils.h"
#define MAX 5000000

using namespace std;
using namespace std::chrono;

long long suma;

bool es_primo(int n){
	if (n<2) return false;
	for(int i=2;i<=sqrt(n);i++){
		if (n%i==0) return false;
	}
	return true;
}

long long sum(int n) {
    long long s=0;
    #pragma omp parallel for reduction(+:s)
    for(int i=2;i<=n;i++) {
        if (es_primo(i)) {
            s+=i;
        }
    }
    return s;
}

int main(int argc, char* argv[]) {
    high_resolution_clock::time_point start, end;
    double timeElapsed;
    cout << "Starting...\n";
    timeElapsed = 0;
    for (int j = 0; j < 1; j++) {
        start = high_resolution_clock::now();
        suma=sum(MAX);
        end = high_resolution_clock::now();
        timeElapsed += duration<double, std::milli>(end - start).count();
    }
    cout<<"suma: "<<suma<<"\n";
    cout << "avg time = " << fixed << setprecision(3) << (timeElapsed / N) << " ms\n";
    return 0;
}
