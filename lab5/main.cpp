#define MS_MPI_NO_SAL
#include <mpi.h>
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int p_rank, p_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &p_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &p_size);

    int size;
    vector<double> A, B, C;

    if (p_rank == 0) {
        ifstream f("matrixA.txt"); f >> size;
        A.resize(size*size); for(int i=0; i<size*size; i++) f >> A[i];
        ifstream f2("matrixB.txt"); f2 >> size;
        B.resize(size*size); for(int i=0; i<size*size; i++) f2 >> B[i];
    }

    MPI_Bcast(&size, 1, MPI_INT, 0, MPI_COMM_WORLD);
    int chunk = size / p_size;
    vector<double> local_A(chunk * size), local_C(chunk * size);
    if (p_rank != 0) B.resize(size * size);

    double start = MPI_Wtime();
    MPI_Bcast(B.data(), size * size, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Scatter(A.data(), chunk * size, MPI_DOUBLE, local_A.data(), chunk * size, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    for (int i = 0; i < chunk; i++) {
        for (int j = 0; j < size; j++) {
            double s = 0;
            for (int k = 0; k < size; k++) s += local_A[i * size + k] * B[k * size + j];
            local_C[i * size + j] = s;
        }
    }

    if (p_rank == 0) C.resize(size * size);
    MPI_Gather(local_C.data(), chunk * size, MPI_DOUBLE, C.data(), chunk * size, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (p_rank == 0) {
        cout << "MPI Processes: " << p_size << " | Time: " << MPI_Wtime() - start << " s" << endl;
        ofstream out("result.txt");
        out << size << endl;
        for(int i=0; i<size*size; i++) out << C[i] << " ";
    }
    MPI_Finalize();
    return 0;
}

