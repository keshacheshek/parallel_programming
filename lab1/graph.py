import matplotlib.pyplot as plt
import numpy as np

sizes = [200, 400, 600, 800, 1200, 1600, 2000]
times = [0.0034592, 0.0339892, 0.162476, 0.478172, 2.38991, 7.60841, 22.5507]

plt.figure(figsize=(12, 7))
plt.plot(sizes, times, marker='o', color='#2c3e50', linewidth=2, label='Последовательный алгоритм')

plt.title('Зависимость времени умножения от размера матрицы', fontsize=14, fontweight='bold')
plt.xlabel('Размерность матрицы (N x N)', fontsize=12)
plt.ylabel('Время (секунды)', fontsize=12)
plt.xticks(np.arange(0, 2001, 200))

plt.grid(True, linestyle='--', alpha=0.7)

plt.xlim(0, 2100)
plt.ylim(-1, max(times) + 3)

plt.savefig('graph.png', dpi=300, bbox_inches='tight')
plt.show()