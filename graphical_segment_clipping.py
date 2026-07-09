import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

coefficients = []
a = None
b = None
epsilon = None

def load_from_file():
    try:
        with open("maindata.txt", "r") as f:
            lines = f.readlines()

            # Рядок 1: коефіцієнти
            c0, c1, c2, c3 = map(float, lines[0].split())
            # Рядок 2: інтервал
            a, b = map(float, lines[1].split())
            # Рядок 3: точність
            epsilon = float(lines[2].strip())

            # Запис у поля
            entry_c0.delete(0, tk.END)
            entry_c0.insert(0, str(c0))

            entry_c1.delete(0, tk.END)
            entry_c1.insert(0, str(c1))

            entry_c2.delete(0, tk.END)
            entry_c2.insert(0, str(c2))

            entry_c3.delete(0, tk.END)
            entry_c3.insert(0, str(c3))

            entry_a.delete(0, tk.END)
            entry_a.insert(0, str(a))

            entry_b.delete(0, tk.END)
            entry_b.insert(0, str(b))

            entry_epsilon.delete(0, tk.END)
            entry_epsilon.insert(0, str(epsilon))

            result_text.insert(tk.END, " Дані успішно завантажено з maindata.txt\n")
    except Exception as e:
        result_text.insert(tk.END, f" Помилка завантаження: {e}\n")

def get_input_data():
    global coefficients, a, b, epsilon
    try:
        c0 = float(entry_c0.get())
        c1 = float(entry_c1.get())
        c2 = float(entry_c2.get())
        c3 = float(entry_c3.get())
        coefficients = [c0, c1, c2, c3]

        a_val = float(entry_a.get())
        b_val = float(entry_b.get())
        if a_val >= b_val:
            messagebox.showerror("Помилка", "Початок інтервалу має бути меншим за кінець.")
            return False
        a = a_val
        b = b_val

        eps_val = float(entry_epsilon.get())
        if eps_val <= 0:
            messagebox.showerror("Помилка", "Точність ε має бути додатним числом.")
            return False
        epsilon = eps_val

        return True
    except ValueError:
        messagebox.showerror("Помилка", "Введіть коректні числові значення.")
        return False

def f(x):
    return coefficients[0] * x**3 + coefficients[1] * x**2 + coefficients[2] * x + coefficients[3]

def isolate_roots():
    # Ізоляція коренів (ділимо інтервал з кроком 0.1)
    step = 0.1
    intervals = []
    x = a
    while x + step <= b:
        if f(x) * f(x + step) < 0:
            intervals.append((x, x + step))
        x += step
    return intervals

def print_intervals(intervals):
    if not intervals:
        result_text.insert(tk.END, "Не знайдено ізольованих інтервалів з коренями.\n")
        return False
    result_text.insert(tk.END, f"Знайдено {len(intervals)} ізольованих інтервалів з можливими коренями:\n")
    for i, (start, end) in enumerate(intervals, 1):
        result_text.insert(tk.END, f"  Інтервал {i}: [{start:.4f}; {end:.4f}]\n")
    return True

def method_dichotomy():
    result_text.delete('1.0', tk.END)
    if not get_input_data():
        return
    result_text.insert(tk.END, "\n=== Метод дихотомії ===\n")
    intervals = isolate_roots()
    if not print_intervals(intervals):
        return

    def dichotomy_verbose(f, left, right, eps):
        iterations = 0
        while abs(right - left) >= 2 * eps:
            iterations += 1
            mid = (left + right) / 2
            f_left = f(left)
            f_mid = f(mid)
            if f_mid == 0:
                left = right = mid
                break
            elif f_left * f_mid < 0:
                right = mid
            else:
                left = mid
        root = (left + right) / 2
        return root, iterations

    roots = []
    iterations_list = []
    for interval in intervals:
        root, iters = dichotomy_verbose(f, interval[0], interval[1], epsilon)
        roots.append(root)
        iterations_list.append(iters)

    result_text.insert(tk.END, f"\nЗнайдені корені (ε = {epsilon}):\n")
    for i, (root, iters) in enumerate(zip(roots, iterations_list), 1):
        result_text.insert(tk.END, f"  Корінь {i}: x = {root:.6f}, f(x) = {f(root):.2e}, ітерацій: {iters}\n")

def method_fibonacci():
    result_text.delete('1.0', tk.END)
    if not get_input_data():
        return
    result_text.insert(tk.END, "\n=== Метод Фібоначчі ===\n")
    intervals = isolate_roots()
    if not print_intervals(intervals):
        return

    def fibonacci_verbose(f, left, right, eps):
        iterations = 0
        a_fib, b_fib = 1, 1
        while abs(right - left) >= 2 * eps:
            iterations += 1
            ratio = a_fib / (a_fib + b_fib)
            x = left + (right - left) * ratio
            f_left = f(left)
            f_x = f(x)
            if f_x == 0:
                left = right = x
                break
            elif f_left * f_x < 0:
                right = x
            else:
                left = x
            a_fib, b_fib = b_fib, a_fib + b_fib
        root = (left + right) / 2
        return root, iterations

    roots = []
    iterations_list = []
    for interval in intervals:
        root, iters = fibonacci_verbose(f, interval[0], interval[1], epsilon)
        roots.append(root)
        iterations_list.append(iters)

    result_text.insert(tk.END, f"\nЗнайдені корені (ε = {epsilon}):\n")
    for i, (root, iters) in enumerate(zip(roots, iterations_list), 1):
        result_text.insert(tk.END, f"  Корінь {i}: x = {root:.6f}, f(x) = {f(root):.2e}, ітерацій: {iters}\n")

def method_golden_section():
    result_text.delete('1.0', tk.END)
    if not get_input_data():
        return
    result_text.insert(tk.END, "\n=== Метод золотого перетину ===\n")
    intervals = isolate_roots()
    if not print_intervals(intervals):
        return

    def golden_section_verbose(f, left, right, eps):
        phi = 0.618
        iterations = 0
        while abs(right - left) >= 2 * eps:
            iterations += 1
            x = left + phi * (right - left)
            fx = f(x)
            f_left = f(left)
            if fx == 0:
                left = right = x
                break
            elif f_left * fx < 0:
                right = x
            else:
                left = x
        root = (left + right) / 2
        return root, iterations

    roots = []
    iterations_list = []
    for interval in intervals:
        root, iters = golden_section_verbose(f, interval[0], interval[1], epsilon)
        roots.append(root)
        iterations_list.append(iters)

    result_text.insert(tk.END, f"\nЗнайдені корені (ε = {epsilon}):\n")
    for i, (root, iters) in enumerate(zip(roots, iterations_list), 1):
        result_text.insert(tk.END, f"  Корінь {i}: x = {root:.6f}, f(x) = {f(root):.2e}, ітерацій: {iters}\n")

def plot_function():
    if not get_input_data():
        return
    xs = np.linspace(a, b, 400)
    ys = f(xs)
    plt.figure(figsize=(6,4))
    plt.axhline(0, color='black', linewidth=0.7)
    plt.plot(xs, ys, label='f(x)')
    plt.title('Графік кубічної функції')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

root = tk.Tk()
root.title("Пошук коренів кубічної функції")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

# Вхідні дані
ttk.Label(frame, text="Коефіцієнт при x³ (c0):").grid(row=0, column=0, sticky="w")
entry_c0 = ttk.Entry(frame, width=10)
entry_c0.grid(row=0, column=1)

ttk.Label(frame, text="Коефіцієнт при x² (c1):").grid(row=1, column=0, sticky="w")
entry_c1 = ttk.Entry(frame, width=10)
entry_c1.grid(row=1, column=1)

ttk.Label(frame, text="Коефіцієнт при x (c2):").grid(row=2, column=0, sticky="w")
entry_c2 = ttk.Entry(frame, width=10)
entry_c2.grid(row=2, column=1)

ttk.Label(frame, text="Вільний член (c3):").grid(row=3, column=0, sticky="w")
entry_c3 = ttk.Entry(frame, width=10)
entry_c3.grid(row=3, column=1)

ttk.Label(frame, text="Початок інтервалу (a):").grid(row=4, column=0, sticky="w")
entry_a = ttk.Entry(frame, width=10)
entry_a.grid(row=4, column=1)

ttk.Label(frame, text="Кінець інтервалу (b):").grid(row=5, column=0, sticky="w")
entry_b = ttk.Entry(frame, width=10)
entry_b.grid(row=5, column=1)

ttk.Label(frame, text="Точність (ε):").grid(row=6, column=0, sticky="w")
entry_epsilon = ttk.Entry(frame, width=10)
entry_epsilon.grid(row=6, column=1)

# Кнопки
btn_plot = ttk.Button(frame, text="Побудувати графік", command=plot_function)
btn_plot.grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")

btn_dichotomy = ttk.Button(frame, text="Метод дихотомії", command=method_dichotomy)
btn_dichotomy.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

btn_fibonacci = ttk.Button(frame, text="Метод Фібоначчі", command=method_fibonacci)
btn_fibonacci.grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")

btn_golden = ttk.Button(frame, text="Метод золотого перетину", command=method_golden_section)
btn_golden.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")

btn_load = ttk.Button(frame, text="Завантажити з файлу", command=load_from_file)
btn_load.grid(row=11, column=0, columnspan=2, pady=5, sticky="ew")

# Текстове поле для виводу
result_text = tk.Text(root, height=15, width=60)
result_text.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()