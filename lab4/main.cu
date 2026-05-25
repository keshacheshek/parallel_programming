#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <cuda_runtime.h>

// Размер блока потоков (16x16 = 256 потоков)
#define TILE_SIZE 16

// Ядро для вычислений на видеокарте (использует быструю Shared Memory)
__global__ void matrixMulKernel(float* A, float* B, float* C, int N) {
    __shared__ float sA[TILE_SIZE][TILE_SIZE];
    __shared__ float sB[TILE_SIZE][TILE_SIZE];

    int tx = threadIdx.x; 
    int ty = threadIdx.y;
    int row = blockIdx.y * TILE_SIZE + ty;
    int col = blockIdx.x * TILE_SIZE + tx;

    float val = 0;
    for (int m = 0; m < N / TILE_SIZE; ++m) {
        // Загрузка данных из медленной глобальной памяти в быструю Shared
        sA[ty][tx] = A[row * N + (m * TILE_SIZE + tx)];
        sB[ty][tx] = B[(m * TILE_SIZE + ty) * N + col];
        __syncthreads(); // Ждем, пока весь блок загрузит данные

        for (int k = 0; k < TILE_SIZE; ++k)
            val += sA[ty][k] * sB[k][tx];
        __syncthreads(); // Ждем окончания вычислений перед новой загрузкой
    }
    if (row < N && col < N) {
        C[row * N + col] = val;
    }
}

int main(int argc, char** argv) {
    // Берем размер матрицы из аргументов или 1024 по умолчанию
    int N = (argc > 1) ? atoi(argv[1]) : 1024;
    
    if (N % TILE_SIZE != 0) {
        std::cout << "Error: N must be multiple of " << TILE_SIZE << std::endl;
        return 1;
    }

    size_t bytes = N * N * sizeof(float);

    // Выделение памяти на процессоре (Host)
    float *h_A = (float*)malloc(bytes);
    float *h_B = (float*)malloc(bytes);
    float *h_C = (float*)malloc(bytes);
    
    // Заполнение случайными числами
    for(int i = 0; i < N * N; i++) {
        h_A[i] = (float)rand() / RAND_MAX;
        h_B[i] = (float)rand() / RAND_MAX;
    }

    // Выделение памяти на видеокарте (Device)
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    // Копирование данных на видеокарту
    cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice);

    // Настройка сетки потоков
    dim3 block(TILE_SIZE, TILE_SIZE);
    dim3 grid(N / TILE_SIZE, N / TILE_SIZE);

    // Создание таймеров CUDA
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    
    // ЗАПУСК ВЫЧИСЛЕНИЙ
    matrixMulKernel<<<grid, block>>>(d_A, d_B, d_C, N);
    
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float ms = 0;
    cudaEventElapsedTime(&ms, start, stop);

    std::cout << "Matrix: " << N << "x" << N << " | Time: " << ms << " ms" << std::endl;
    
    // Освобождение ресурсов
    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    free(h_A); free(h_B); free(h_C);
    
    return 0;
}
