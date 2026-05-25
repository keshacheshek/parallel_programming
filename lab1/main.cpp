#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>

using namespace std;

typedef vector<double> Row;
typedef vector<Row> Matrix;

Matrix load_data(string path, int& dim) {
    ifstream input(path.c_str());
    if (!input) return {};
    input >> dim;
    Matrix m(dim, Row(dim));
    for (int i = 0; i < dim; i++)
        for (int j = 0; j < dim; j++)
            input >> m[i][j];
    return m;
}

int main() {
    int N;
    Matrix mat1 = load_data("matrixA.txt", N);
    Matrix mat2 = load_data("matrixB.txt", N);

    if (mat1.empty()) return 1;

    Matrix res(N, Row(N, 0.0));
    auto start = chrono::steady_clock::now();

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                res[i][j] += mat1[i][k] * mat2[k][j];
            }
        }
    }

    auto end = chrono::steady_clock::now();
    chrono::duration<double> elapsed = end - start;

    cout << "Size: " << N << " | Time: " << elapsed.count() << " s" << endl;

    ofstream out("result.txt");
    out << N << endl;
    for (auto& row : res) {
        for (double val : row) out << val << " ";
        out << endl;
    }
    return 0;
}
