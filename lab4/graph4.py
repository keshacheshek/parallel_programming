import matplotlib.pyplot as plt
import numpy as np

sizes = [512, 1024, 2048]
kernel_time = [0.43, 3.68, 31.89]
cublas_time = [0.51, 1.83, 5.70]

plt.figure(figsize=(10, 6))

plt.plot(sizes, kernel_time, marker='o', label='Optimized Kernel (Shared Memory)', color='#e74c3c', linewidth=2)
plt.plot(sizes, cublas_time, marker='s', label='NVIDIA cuBLAS', color='#2ecc71', linewidth=2)

plt.title('Сравнение производительности: Ручное ядро vs cuBLAS', fontsize=14)
plt.xlabel('Размер матрицы (N x N)', fontsize=12)
plt.ylabel('Время выполнения (мс)', fontsize=12)

plt.xticks(sizes)
plt.yscale('log')
plt.grid(True, which="both", linestyle='--', alpha=0.5)

for i in range(len(sizes)):
    plt.text(sizes[i], kernel_time[i], f'{kernel_time[i]}ms', ha='right', va='bottom', fontsize=9)
    plt.text(sizes[i], cublas_time[i], f'{cublas_time[i]}ms', ha='right', va='top', fontsize=9)

plt.legend()
plt.tight_layout()

plt.savefig('cuda_graph.png', dpi=300)
plt.show()