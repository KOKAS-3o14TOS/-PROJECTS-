#include <iostream>
#include <iomanip>
#include <chrono>
#include <cmath>
#include <vector>
#include "utils.h"
using namespace std;
using namespace std::chrono;

////////////////////////////////////////funciones/////////////////////////////////////////////
const int THREADS=8;
vector<int> numeros={1,8,3,7,0,9,5,6};
int X=numeros.size();

typedef struct{
	int start, end;
	long long suma_hilo;
}
Block;

bool es_par(int n){
	if (n%2==0) return true;
	return false;
}

void* task(void* params){
	Block* block_i;
	long long suma;
	block_i=(Block*) params;
	suma=0;
	for(int i=block_i->start;i<block_i->end;i++){
		if (es_par(numeros[i])){
			suma+=numeros[i];
		}
	}
	block_i->suma_hilo=suma;
	pthread_exit(0);
}
/////////////////////////////////////////////////////////////////////////////////////

int main(int argc, char* argv[]) {
	long long result = 0;
	////////////////////////////////////////bloques/////////////////////////////////////////////
	pthread_t tid[THREADS];
	Block blocks[THREADS];
	int block_size;
	block_size = X / THREADS;
	for(int i = 0; i < THREADS; i++){
		blocks[i].start = i * block_size;
		if (i!=(THREADS-1)) blocks[i].end=(i+1)*block_size;
		else blocks[i].end=X+1;
	}
	/////////////////////////////////////////////////////////////////////////////////////
	high_resolution_clock::time_point start, end;
	double timeElapsed;
	cout << "Starting...\n";
	timeElapsed = 0;
	for (int j = 0; j < N; j++) {
		result = 0;
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
