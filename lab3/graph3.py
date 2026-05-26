import matplotlib.pyplot as plt
import numpy as np

sizes = [600, 1200, 1600]
procs = [1, 2, 4, 6, 12]

time_data = [
    [0.111024, 0.0585902, 0.0518055, 0.050834, 0.041261],
    [1.92964, 1.63331, 1.12144, 1.00304, 0.959468],
    [6.616, 4.22438, 2.82081, 2.37644, 2.30873]
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 1. График времени
for i, s_size in enumerate(sizes):
    ax1.plot(procs, time_data[i], marker='o', label=f'Size {s_size}')

ax1.set_title('Время выполнения MPI')
ax1.set_xlabel('Количество процессов')
ax1.set_ylabel('Время (сек)')
ax1.set_xticks(procs)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# 2. График ускорения
for i, s_size in enumerate(sizes):
    t1 = time_data[i][0]
    speedup = [t1 / tp for tp in time_data[i]]
    ax2.plot(procs, speedup, marker='s', label=f'Size {s_size}')

ax2.plot(procs, procs, color='black', linestyle='--', alpha=0.3, label='Идеальное')
ax2.set_title('Ускорение (Speedup) MPI')
ax2.set_xlabel('Количество процессов')
ax2.set_ylabel('S = T1 / Tp')
ax2.set_xticks(procs)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.savefig('mpi_graph.png', dpi=300)
plt.show()