#include <iostream>
#include <iomanip>
#include <chrono>
#include <cmath>
#include <vector>
#include "utils.h"
#define MAXIMUM 5000000
using namespace std;
using namespace std::chrono;

////////////////////////////////////////funciones/////////////////////////////////////////////
const int THREADS=8;

typedef struct{
	int start, end;
	long long suma_hilo;
}
Block;

bool es_primo(int n){
	if (n<2) return false;
	for(int i=2;i<=sqrt(n);i++){
		if (n%i==0) return false;
	}
	return true;
}

void* task(void* param){
    long long suma=0;
	Block* block_i;
	block_i=(Block*) param;
	for(int i=block_i->start;i<block_i->end;i++){
		if (es_primo(i)){
			suma+=i;
		}
	}
	block_i->suma_hilo=suma;
	pthread_exit(0);
}
/////////////////////////////////////////////////////////////////////////////////////

int main(int argc, char* argv[]) {
	long long result=0;
	////////////////////////////////////////bloques/////////////////////////////////////////////
	pthread_t tid[THREADS];
	Block blocks[THREADS];
	int elementos=MAXIMUM/THREADS;
	for(int i=0;i<THREADS;i++){
		blocks[i].start=i*elementos;
		if (i!=(THREADS-1)) blocks[i].end=(i+1)*elementos;
		else blocks[i].end=MAXIMUM+1;
	}
	/////////////////////////////////////////////////////////////////////////////////////
	high_resolution_clock::time_point start, end;
	double timeElapsed;
	cout << "Starting...\n";
	timeElapsed = 0;
	for (int j = 0; j < N; j++) {
		result=0;
		start = high_resolution_clock::now();
		////////////////////////////////////////llama función/////////////////////////////////////////////
		for(int i=0;i<THREADS;i++){
			pthread_create(&tid[i],NULL,task,&blocks[i]);
		}
		for(int i=0;i<THREADS;i++){
			pthread_join(tid[i],NULL);
			result+=blocks[i].suma_hilo;
		}
		/////////////////////////////////////////////////////////////////////////////////////
		end = high_resolution_clock::now();
		timeElapsed += duration<double, std::milli>(end - start).count();
	}
	cout << "result = " << result << "\n";
	cout << "avg time = " << fixed << setprecision(3) << (timeElapsed / N) <<  " ms\n";
	return 0;
}
