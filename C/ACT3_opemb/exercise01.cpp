/*
Desarrolla una función que recibe como parámetros un arreglo de números enteros y el tamaño del mismo. 
La función regresa la sumatoria de todos los elementos pares contenidos en el arreglo. 
El arreglo esperado para el arreglo creado en el código base es 500000000.

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
int SIZE = 5000000;
int variable;

int SumPares(int *array,int size) {
    int pares=0;
    #pragma omp parallel for reduction(+:pares)
    for(int i=0;i<size;i++){
        if(array[i]%2==0){
            pares+=1;
        }
    }
    return pares;
}

int main()
{
    int *array;
    double timeElapsed = 0;
    array = new int[SIZE];

    for(int i=0;i<SIZE;i++){
        array[i]=i;
    }

    high_resolution_clock::time_point START, END;
     /* Asignamos por cada hilo su inicio y fin */
    for (int i = 0; i < THREADS; i++) {
        START = high_resolution_clock::now();
        variable = SumPares(array,SIZE);
        END = high_resolution_clock::now();
        timeElapsed += duration<double, milli>(END - START).count();
    }

    cout <<"Total  "<< variable <<" Time:"<< timeElapsed/THREADS <<endl;

    return 0;

}