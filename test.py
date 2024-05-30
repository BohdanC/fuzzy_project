import numpy as np
from matplotlib import pyplot as plt
from main import systolic_func, diastolic_func, pulse_func, calculate_blood_pressure

np.random.seed(seed=2024)
USE_NOISE = 0  # 1 = використання шуму, 0 = відсутність шуму

# Визначення часового проміжку
num = 100
time = np.linspace(start=0, stop=1, num=num)

# Зміна систолічного тиску з часом + шум
systolic = (180 - 80) * 0.8 * time + 90 + 3 * np.random.randn(num) * USE_NOISE

# Зміна діастолічного тиску з часом + шум
diastolic = (120 - 50) * 0.8 * time + 60 + 2 * np.random.randn(num) * USE_NOISE

# Зміна пульсу з часом + шум
pulse = (180 - 40) * 0.8 * time + 50 + 3 * np.random.randn(num) * USE_NOISE

# Обчислення оцінки артеріального тиску у часі
blood_pressure = [calculate_blood_pressure(systolic_value=systolic[t],
                                           diastolic_value=diastolic[t],
                                           pulse_value=pulse[t]) for t in range(num)]



# Plotting the membership functions for systolic, diastolic, and pulse as in slide 4
x_systolic = np.linspace(60, 200, 400)
x_diastolic = np.linspace(40, 140, 400)
x_pulse = np.linspace(30, 190, 400)

systolic_low = [systolic_func(value)['low'] for value in x_systolic]
systolic_normal = [systolic_func(value)['normal'] for value in x_systolic]
systolic_high = [systolic_func(value)['high'] for value in x_systolic]

diastolic_low = [diastolic_func(value)['low'] for value in x_diastolic]
diastolic_normal = [diastolic_func(value)['normal'] for value in x_diastolic]
diastolic_high = [diastolic_func(value)['high'] for value in x_diastolic]

pulse_low = [pulse_func(value)['low'] for value in x_pulse]
pulse_normal = [pulse_func(value)['normal'] for value in x_pulse]
pulse_high = [pulse_func(value)['high'] for value in x_pulse]

plt.figure(figsize=(15, 10))

plt.subplot(3, 1, 1)
plt.plot(x_systolic, systolic_low, label='Low', color='tab:blue')
plt.plot(x_systolic, systolic_normal, label='Normal', color='tab:green')
plt.plot(x_systolic, systolic_high, label='High', color='tab:red')
plt.axhline(0, color='black', linewidth=3)
plt.title('Систолічний тиск')
plt.xlabel('Значення')
plt.ylabel('Належність')
plt.legend()
plt.xlim(80, 180)

plt.subplot(3, 1, 2)
plt.plot(x_diastolic, diastolic_low, label='Low', color='tab:blue')
plt.plot(x_diastolic, diastolic_normal, label='Normal', color='tab:green')
plt.plot(x_diastolic, diastolic_high, label='High', color='tab:red')
plt.axhline(0, color='black', linewidth=3)
plt.title('Діастолічний тиск')
plt.xlabel('Значення')
plt.ylabel('Належність')
plt.legend()
plt.xlim(50, 120)

plt.subplot(3, 1, 3)
plt.plot(x_pulse, pulse_low, label='Low', color='tab:blue')
plt.plot(x_pulse, pulse_normal, label='Normal', color='tab:green')
plt.plot(x_pulse, pulse_high, label='High', color='tab:red')
plt.axhline(0, color='black', linewidth=3)
plt.title('Пульс')
plt.xlabel('Значення')
plt.ylabel('Належність')
plt.legend()
plt.xlim(40, 180)

plt.tight_layout()
plt.show()


# Відображення графіку
plt.figure(figsize=(10, 8))

plt.subplot(5, 1, 1)
plt.plot(systolic, color="tab:blue")
plt.axhline(0, color='black', linewidth=1)
plt.ylabel('Систолічний')
plt.ylim(80, 180)
plt.xticks([])

plt.subplot(5, 1, 2)
plt.plot(diastolic, color="tab:orange")
plt.axhline(0, color='black', linewidth=1)
plt.ylabel('Діастолічний')
plt.ylim(50, 120)
plt.xticks([])

plt.subplot(5, 1, 3)
plt.plot(pulse, color="tab:green")
plt.axhline(0, color='black', linewidth=1)
plt.ylabel('Пульс')
plt.ylim(40, 180)
plt.xticks([])

plt.subplot(5, 1, (4, 5))
plt.plot(blood_pressure, color="tab:purple")
plt.axhline(0, color='black', linewidth=1)
plt.title('Оцінка артеріального тиску')
plt.xticks([])

plt.tight_layout()
plt.show()
