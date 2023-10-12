/*
Desarrolla un procedimiento que recibe como parámetros un arreglo de enteros y el tamaño del mismo.
El procedimiento ordena los elementos del arreglo de manera ascendente (de menor a mayor) 
usando el algoritmo de ordenamiento conocido como Enumeration Sort.

Jorge Martínez Lopez A01704518
Gaddiel Lara Roldán A01704231

*/
#include <iostream>
#include <iomanip>
#include <chrono>
#include <omp.h>
#include "utils.h"

using namespace std;
using namespace chrono;

const int THREADS = 4;
int SIZE = 100000;
 

/*La función sort*/
void Sort(int *a,int *b, int size) {
    #pragma omp parallel for
    for (int i = 0; i < size; ++i) {
        int k = 0;
        for (int j = 0; j < size; ++j) {
            if (a[j] < a[i] || (a[j] == a[i] && j < i)) {
                k++;
            }
        }
        b[k] = a[i];
    }
}


int main()
{

    int *a, *b;
    double timeElapsed = 0;
    a = new int[SIZE];
    b = new int[SIZE];

    for(int i=0;i<SIZE;i++){
        a[i]=i;
    }
    high_resolution_clock::time_point START, END;
     /* Asignamos por cada hilo su inicio y fin */
    
    for (int i = 0; i < THREADS; i++) {
        START = high_resolution_clock::now();
        Sort(a,b,SIZE);
        END = high_resolution_clock::now();
        timeElapsed += duration<double, milli>(END - START).count();
    }

    cout <<" Time:"<< timeElapsed/THREADS <<endl;
    return 0;
}