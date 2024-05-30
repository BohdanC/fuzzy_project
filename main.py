import numpy as np
import tkinter as tk
from tkinter import messagebox


# Трапецієвидна функцій належності
def trapmf(x, a, b, c, d):
    if a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c < x < d:
        return (x - d) / (c - d)
    else:
        return 0


# Визначення функцій належності для систолічного тиску
def systolic_func(value):
    data = {'low': trapmf(value, a=80, b=80, c=90, d=110),
            'normal': trapmf(value, a=90, b=120, c=120, d=140),
            'high': trapmf(value, a=130, b=160, c=180, d=180)}
    return data


# Визначення функцій належності для діастолічного тиску
def diastolic_func(value):
    data = {'low': trapmf(value, a=50, b=50, c=60, d=80),
            'normal': trapmf(value, a=60, b=80, c=80, d=100),
            'high': trapmf(value, a=80, b=100, c=120, d=120)}
    return data


# Визначення функцій належності для пульсу
def pulse_func(value):
    data = {'low': trapmf(value, a=40, b=40, c=50, d=70),
            'normal': trapmf(value, a=50, b=70, c=70, d=90),
            'high': trapmf(value, a=80, b=120, c=180, d=180)}
    return data


# Визначення функцій належності для оцінки артеріального тиску
def blood_pressure_func(value):
    data = {'low': trapmf(value, a=0, b=0, c=20, d=50),
            'normal': trapmf(value, a=20, b=50, c=50, d=80),
            'high': trapmf(value, a=50, b=80, c=100, d=100)}
    return data


# Визначення правил нечіткої системи
def calculate_rules(systolic, diastolic, pulse):
    return [
        # Правило 1: Якщо (систолічний = high і діастолічний = high) або пульс = high, то оцінка = high
        ('high', max(min(systolic['high'], diastolic['high']), pulse['high'])),

        # Правило 2: Якщо систолічний = normal і діастолічний = normal і пульс = normal, то оцінка = normal
        ('normal', min(systolic['normal'], diastolic['normal'], pulse['normal'])),

        # Правило 3: Якщо (систолічний = low і діастолічний = low) або пульс = low, то оцінка = low.
        ('low', max(min(systolic['low'], diastolic['low']), pulse['low'])),

        # Правило 4: Якщо систолічний = normal і діастолічний = normal і пульс = high, то оцінка = normal
        ('normal', min(systolic['normal'], diastolic['normal'], pulse['high'])),
    ]


# Імплікації відповідних правил (Мамдані)
def calculate_implication(rules):
    num = 100
    blood_pressure_values = np.linspace(start=0, stop=100, num=num)
    blood_pressure_fuzzy = {'low': np.zeros(num), 'normal': np.zeros(num), 'high': np.zeros(num)}

    for i in range(num):
        fuzzy_output = blood_pressure_func(value=blood_pressure_values[i])
        blood_pressure_fuzzy['low'][i] = fuzzy_output['low']
        blood_pressure_fuzzy['normal'][i] = fuzzy_output['normal']
        blood_pressure_fuzzy['high'][i] = fuzzy_output['high']

    result = {'low': np.zeros(num), 'normal': np.zeros(num), 'high': np.zeros(num)}
    counter = {'low': 0, 'normal': 0, 'high': 0}
    for name, value in rules:
        result[name] += np.minimum(value, blood_pressure_fuzzy[name])
        counter[name] += 1

    for key in result.keys():
        result[key] /= counter[key]
    return result


# Агрегації результатів імплікації правил
def calculate_aggregation(implication):
    result = np.zeros_like(implication[list(implication.keys())[0]])
    for name, value in implication.items():
        result = np.maximum(result, value)
    return result


# Проведення дефазифікації результатів
def calculate_defuzzification(aggregation):
    num = len(aggregation)
    blood_pressure_values = np.linspace(start=0, stop=100, num=num)

    a, b = 0, 0
    for i in range(num):
        if aggregation[i] > 0:
            a += aggregation[i] * blood_pressure_values[i]
            b += aggregation[i]
    return a / b if not b == 0 else None


# Функція для обчислення оцінки артеріального тиску
def calculate_blood_pressure(systolic_value, diastolic_value, pulse_value):
    # Проведення фазифікації вхідних параметрів
    systolic_fuzzy = systolic_func(value=systolic_value)
    diastolic_fuzzy = diastolic_func(value=diastolic_value)
    pulse_fuzzy = pulse_func(value=pulse_value)

    # Обчислення відповідних правил
    rules = calculate_rules(systolic=systolic_fuzzy, diastolic=diastolic_fuzzy, pulse=pulse_fuzzy)

    # Обчислення імплікації за Мамдані
    implication = calculate_implication(rules=rules)

    # Проведення агрегації вілповідних результатів
    aggregation = calculate_aggregation(implication=implication)

    # Дефазивікація ортиманої оцінки кровяного тиску
    blood_pressure_score = calculate_defuzzification(aggregation=aggregation)

    if blood_pressure_score is None:
        return 777
    return blood_pressure_score


def interface():
    try:
        systolic_value = float(entry_systolic.get())
        diastolic_value = float(entry_diastolic.get())
        pulse_value = float(entry_pulse.get())

        if not (80 <= systolic_value <= 180):
            messagebox.showerror('Помилка', 'Межі систолічного тиску: 80 - 180')

        if not (50 <= diastolic_value <= 120):
            messagebox.showerror('Помилка', 'Межі діастолічного тиску: 50 - 120')

        if not (40 <= pulse_value <= 180):
            messagebox.showerror('Помилка', 'Межі пульсу: 40 - 180')

        result = calculate_blood_pressure(
            systolic_value=systolic_value,
            diastolic_value=diastolic_value,
            pulse_value=pulse_value
        )
        messagebox.showinfo('Результат', f'Оцінка артеріального тиску: {result:.2f}')
    except ValueError:
        messagebox.showerror('Помилка', 'Будь ласка, введіть числові значення для всіх полів.')


if __name__ == '__main__':
    # Створення графічного інтерфейсу користувача
    root = tk.Tk()
    root.title('Оцінка артеріального тиску')

    tk.Label(root, text='Систолічний тиск').grid(row=0, column=0)
    entry_systolic = tk.Entry(root)
    entry_systolic.grid(row=0, column=1)

    tk.Label(root, text='Діастолічний тиск').grid(row=1, column=0)
    entry_diastolic = tk.Entry(root)
    entry_diastolic.grid(row=1, column=1)

    tk.Label(root, text='Пульс').grid(row=2, column=0)
    entry_pulse = tk.Entry(root)
    entry_pulse.grid(row=2, column=1)

    tk.Button(root, text='Обчислити', command=interface).grid(row=3, column=0, columnspan=2)
    root.mainloop()
