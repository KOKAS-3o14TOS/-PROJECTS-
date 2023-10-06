#include <iostream>
#include <vector>
#include <thread>

const int THREADS = 4;

using namespace std;
vector<int> principal = {1, 8, 3, 7, 0, 9, 5, 6};
vector<int> aux(principal.size());
int SIZE = principal.size();

/*La función sort*/
void Sort(vector<int> &a, vector<int> &b, int start, int end) {
    for (int i = start; i < end; ++i) {
        int k = 0;
        for (int j = 0; j < SIZE; ++j) {
            if (a[j] < a[i] || (a[j] == a[i] && j < i)) {
                k++;
            }
        }
        b[k] = a[i];
    }
}

int main() {
    vector<thread> threads;
    /* Crea el tamaño de los bloques*/
    int blocks = SIZE / THREADS;
    /* Asignamos por cada hilo su inicio y fin */
    for (int i = 0; i < THREADS; i++) {
        int start = i * blocks;
        int end = start + blocks;
        /*Añade al vector un thread y un ref llama a otros elementos*/
        threads.emplace_back(Sort, ref(principal), ref(aux), start, end);
    }
    /*Crea por cada thread un join*/
    for (int i=0;i<threads.size();i++) {
        threads[i].join();
    }
    /*Hace la copia en el principal*/
    principal = aux;
    /*Printea cada elemento*/
    for (int i = 0; i < SIZE; ++i) {
        cout << principal[i] << " ";
    }
    cout << endl;

    return 0;
}
