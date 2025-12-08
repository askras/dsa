# +
import numpy as np
import matplotlib.pyplot as plt

# Параметры уравнения
alpha = 350.0       # 1/с
omega = 614.4       # рад/с
A = -15.75          # коэф. при cos
B = -8.17           # коэф. при sin
i_pr_val = -43.75   # принуждённая составляющая

tau = 1 / alpha     # ≈ 0.002857 с
t_max = 0.018       # 18 мс (> 6τ)

# Время
t_before = np.linspace(-0.005, 0, 100)
t_after = np.linspace(0, t_max, 3000)
t_full = np.concatenate([t_before, t_after])

# Принуждённая составляющая (постоянна)
i_pr = np.full_like(t_full, i_pr_val)

# Свободная составляющая
i_sv_before = np.zeros_like(t_before)  # до коммутации нет переходного процесса
i_sv_after = np.exp(-alpha * t_after) * (A * np.cos(omega * t_after) + B * np.sin(omega * t_after))
i_sv_full = np.concatenate([i_sv_before, i_sv_after])

# Полный ток
i_full = i_pr + i_sv_full

# Проверка значений
i0_plus = i_full[len(t_before)]  # первое значение при t >= 0
print(f"i(0+) = {i0_plus:.3f} А (ожидается: {A + i_pr_val:.3f} = {-15.75 - 43.75:.3f} А)")
print(f"i(∞) = {i_pr_val} А")
print(f"i_sv(0+) = {i_sv_full[len(t_before)]:.3f} А (ожидается: {A} А)")

# Построение
plt.figure(figsize=(13, 7))

plt.plot(t_full, i_full,      'b-',  linewidth=2.5, label=r'Полный ток $i(t) = i_{\text{пр}} + i_{\text{св}}$')
plt.plot(t_full, i_pr,        'r--', linewidth=1.8, label=rf'Принуждённая: $i_{{\text{{пр}}}} = {i_pr_val}\ \text{{А}}$')
plt.plot(t_full, i_sv_full,   'g-.', linewidth=2.0, label=r'Свободная составляющая $i_{\text{св}}(t)$')

# Вертикальные линии
plt.axvline(x=0,      color='k',   linestyle=':', linewidth=1.5, label='Коммутация ($t = 0$)')
plt.axvline(x=3*tau,  color='m',   linestyle=':', linewidth=1.2, label=rf'$t = 3\tau \approx {3*tau*1000:.1f}\ \text{{мс}}$')

# Дополнительно: отметим начальное значение
plt.axhline(y=i0_plus, color='orange', linestyle=':', linewidth=1, alpha=0.7)

# Оформление
plt.axhline(y=0, color='gray', linewidth=0.6, alpha=0.5)
plt.xlabel('Время, с', fontsize=12)
plt.ylabel('Ток $i$, А', fontsize=12)
plt.title(
    r'Переходный процесс: $i(t) = (-15.75 \cos 614.4t - 8.17 \sin 614.4t)\, e^{-350t} - 43.75$',
    fontsize=13, pad=15
)
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(fontsize=10)
plt.xlim(-0.005, t_max)
plt.ylim(-75, 10)  # учитываем отрицательный пик ~ -59.5 А

# Аннотации
plt.text(0.0005,  -40, rf'$i(0_+) = {i0_plus:.1f}\ \text{{А}}$', color='b', fontsize=10)
plt.text(0.0005,  -62, r'$i_{\text{св}}(0_+) = -15.75\ \text{А}$', color='g', fontsize=10)
plt.text(0.0005,  -48, rf'$i_{{\text{{пр}}}} = {i_pr_val}\ \text{{А}}$', color='r', fontsize=10)
plt.text(3*tau + 0.0003, -72, '3τ', color='m', fontsize=9, rotation=90)

# Подпись до коммутации
plt.text(-0.0045, -65, 'До коммутации:\n$i = 0$, $i_{\\text{св}} = 0$', fontsize=9, color='k')

plt.tight_layout()
plt.show()
# -




