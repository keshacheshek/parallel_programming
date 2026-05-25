import matplotlib.pyplot as plt
import numpy as np

sizes = [400, 800, 1200, 1600]
threads = [1, 2, 4, 6, 12]

time_data = [
    [0.029156, 0.0179999, 0.0120001, 0.0109999, 0.00899982],
    [0.378782, 0.282165, 0.121654, 0.118654, 0.0929999],
    [1.622564, 1.046935, 0.64657, 0.59262, 0.541155],
    [8.04316, 3.76821, 2.42968, 1.811853, 1.56915]
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 1. График времени
for i, t in enumerate(threads):
    ax1.plot(sizes, [row[i] for row in time_data], marker='o', label=f'{t} потоков')

ax1.set_title('Время выполнения')
ax1.set_xlabel('Размер матрицы N')
ax1.set_ylabel('Время (сек)')
ax1.set_xticks(np.arange(400, 1601, 200))
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# 2. График ускорения
for i, s_size in enumerate(sizes):
    t1 = time_data[i][0]
    speedup = [t1 / tp for tp in time_data[i]]
    ax2.plot(threads, speedup, marker='s', label=f'Size {s_size}')

ax2.plot(threads, threads, color='black', linestyle='--', alpha=0.5, label='Идеальное')
ax2.set_title('Ускорение (Speedup)')
ax2.set_xlabel('Количество потоков')
ax2.set_ylabel('S = T1 / Tp')
ax2.set_xticks(threads)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.savefig('openmp_graph.png', dpi=300)
plt.show()