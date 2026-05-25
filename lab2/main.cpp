#include <iostream>
#include <vector>
#include <fstream>
#include <omp.h>

using namespace std;

int main(int argc, char** argv) {
    int threads = (argc > 1) ? atoi(argv[1]) : 4;
    int n;
    ifstream fa("matrixA.txt"); fa >> n;
    vector<double> a(n*n), b(n*n), c(n*n, 0);
    for(int i=0; i<n*n; i++) fa >> a[i];
    ifstream fb("matrixB.txt"); fb >> n;
    for(int i=0; i<n*n; i++) fb >> b[i];

    omp_set_num_threads(threads);
    double t_start = omp_get_wtime();

    #pragma omp parallel for collapse(2)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double temp = 0;
            for (int k = 0; k < n; k++) {
                temp += a[i * n + k] * b[k * n + j];
            }
            c[i * n + j] = temp;
        }
    }

    cout << "Threads: " << threads << " | Time: " << omp_get_wtime() - t_start << " s" << endl;
    return 0;
}
