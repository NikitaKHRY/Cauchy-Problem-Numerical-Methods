def main():
    while True:
        print_current_data()
        print("\n=== Меню ===")
        print("1. Ввести дані (вручну або з файлу)")
        print("2. Метод дихотомії")
        print("3. Метод Фібоначчі")
        print("4. Метод золотого перетину")
        print("5. Вихід")

        choice = input("Оберіть пункт меню (1-5): ")

        if choice == '1':
            input_data()
        elif choice == '2':
            method_dichotomy()
        elif choice == '3':
            method_fibonacci()
        elif choice == '4':
            method_golden_section()
        elif choice == '5':
            print("Завершення програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

def print_current_data():
    print("\n=== Поточні дані ===")
    if coefficients:
        print(f"Коефіцієнти рівняння: {coefficients[0]}x^3 + {coefficients[1]}x^2 + {coefficients[2]}x + {coefficients[3]} = 0")
    else:
        print("Коефіцієнти: не задано")

    if a is not None and b is not None:
        print(f"Інтервал: [{a}; {b}]")
    else:
        print("Інтервал: не задано")

    if epsilon is not None:
        print(f"Точність: {epsilon}")
    else:
        print("Точність: не задано")

# Змінні для збереження даних
coefficients = []
a = b = epsilon = None

def input_data():
    global coefficients, a, b, epsilon

    while True:
        print("\n=== Ввід даних ===")
        print("1. Ввести вручну")
        print("2. Зчитати з файлу (maindata.txt)")
        print("3. Назад до головного меню")
        choice = input("Оберіть пункт (1-3): ")

        if choice == '1':
            try:
                print("Введіть коефіцієнти рівняння типу: x^3 – 4.1x^2 + 2.2x + 1.4 = 0")
                coeffs = input("Введіть 4 коефіцієнти через пробіл: ").split()
                if len(coeffs) != 4:
                    raise ValueError("Потрібно ввести рівно 4 коефіцієнти.")
                coefficients = [float(c) for c in coeffs]

                a = float(input("Ліва межа інтервалу (a): "))
                b = float(input("Права межа інтервалу (b): "))
                if a >= b:
                    raise ValueError("Ліва межа має бути меншою за праву.")

                epsilon = float(input("Точність обчислень (ε): "))
                if epsilon <= 0:
                    raise ValueError("Точність повинна бути додатною.")

                print(" Дані збережено.")
                break
            except ValueError as ve:
                print(f" Помилка: {ve}")
            except Exception:
                print(" Помилка: Некоректний ввід. Спробуйте ще раз.")

        elif choice == '2':
            try:
                with open("maindata.txt", "r") as file:
                    lines = file.readlines()
                    if len(lines) < 3:
                        raise ValueError("Файл повинен містити щонайменше 3 рядки.")

                    coeffs = list(map(float, lines[0].strip().split()))
                    if len(coeffs) != 4:
                        raise ValueError("У першому рядку мають бути рівно 4 коефіцієнти.")
                    coefficients = coeffs

                    a_val, b_val = map(float, lines[1].strip().split())
                    if a_val >= b_val:
                        raise ValueError("Ліва межа повинна бути меншою за праву.")
                    a, b = a_val, b_val

                    epsilon_val = float(lines[2].strip())
                    if epsilon_val <= 0:
                        raise ValueError("Точність повинна бути додатною.")
                    epsilon = epsilon_val

                    print(" Дані успішно зчитано з файлу.")
                    break
            except FileNotFoundError:
                print(" Файл maindata.txt не знайдено.")
            except ValueError as ve:
                print(f" Помилка у файлі: {ve}")
            except Exception as e:
                print(f" Загальна помилка: {e}")

        elif choice == '3':
            break
        else:
            print(" Невірний вибір. Спробуйте ще раз.")

def method_dichotomy():
    global coefficients, a, b, epsilon

    if not coefficients or a is None or b is None or epsilon is None:
        print("Дані не задані. Спочатку введіть усі необхідні параметри.")
        return

    def f(x):
        return (coefficients[0] * x**3 +
                coefficients[1] * x**2 +
                coefficients[2] * x +
                coefficients[3])

    print("\n=== Метод дихотомії ===")

    # Ізоляція коренів: ділимо інтервал на кроком 0.1
    x = a
    isolation_intervals = []
    step = 0.1
    while x + step <= b:
        x1 = x
        x2 = x + step
        if f(x1) * f(x2) < 0:
            isolation_intervals.append((x1, x2))
        x += step

    if not isolation_intervals:
        print("Не знайдено ізольованих інтервалів з коренями.")
        return

    print(f"Знайдено {len(isolation_intervals)} ізольованих інтервалів з можливими коренями:")
    for i, (start, end) in enumerate(isolation_intervals, 1):
        print(f"  Інтервал {i}: [{start:.4f}; {end:.4f}]")

    def dichotomy_verbose(f, left, right, eps):
        iterations = 0
        while abs(right - left) >= 2 * eps:
            iterations += 1
            prev_left, prev_right = left, right  # Вхідний інтервал для цієї ітерації

            mid = (left + right) / 2
            f_left = f(left)
            f_mid = f(mid)

            # Вивід вхідного та вихідного інтервалів
            print(f"  Ітерація {iterations}: Вхідний інтервал [{prev_left:.6f}, {prev_right:.6f}]", end=', ')

            if f_mid == 0:
                left = right = mid
                print(f"Вихідний інтервал [{mid:.6f}, {mid:.6f}] (точний корінь знайдено)")
                break
            elif f_left * f_mid < 0:
                right = mid
            else:
                left = mid

            print(f"Вихідний інтервал [{left:.6f}, {right:.6f}]")

        root = (left + right) / 2
        return root, iterations

    roots = []
    iterations_list = []
    for interval in isolation_intervals:
        root, iters = dichotomy_verbose(f, interval[0], interval[1], epsilon)
        roots.append(root)
        iterations_list.append(iters)

    print("\nЗнайдені корені (з точністю ε = {}):".format(epsilon))
    for i, (root, iters) in enumerate(zip(roots, iterations_list), 1):
        print(f"  Корінь {i}: x = {root:.6f}, f(x) = {f(root):.2e}, ітерацій: {iters}")

def method_fibonacci():
    global coefficients, a, b, epsilon

    if not coefficients or a is None or b is None or epsilon is None:
        print("Дані не задані. Спочатку введіть усі необхідні параметри.")
        return

    def f(x):
        return (coefficients[0] * x**3 +
                coefficients[1] * x**2 +
                coefficients[2] * x +
                coefficients[3])

    print("\n=== Метод Фібоначчі (перебором) ===")

    # Ізоляція коренів
    x = a
    isolation_intervals = []
    step = 0.1
    while x + step <= b:
        x1 = x
        x2 = x + step
        if f(x1) * f(x2) < 0:
            isolation_intervals.append((x1, x2))
        x += step

    if not isolation_intervals:
        print("Не знайдено ізольованих інтервалів з коренями.")
        return

    print(f"Знайдено {len(isolation_intervals)} ізольованих інтервалів з можливими коренями:")
    for i, (start, end) in enumerate(isolation_intervals, 1):
        print(f"  Інтервал {i}: [{start:.4f}; {end:.4f}]")

    def fibonacci_verbose(f, left, right, eps):
        iterations = 0
        a_fib, b_fib = 1, 1  # Початкові значення

        while abs(right - left) >= 2 * eps:
            iterations += 1
            prev_left, prev_right = left, right

            ratio = a_fib / (a_fib + b_fib)
            x = left + (right - left) * ratio

            f_left = f(left)
            f_x = f(x)

            print(f"  Ітерація {iterations}: Вхідний інтервал [{prev_left:.6f}, {prev_right:.6f}], ", end='')

            if f_x == 0:
                left = right = x
                print(f"Вихідний інтервал [{x:.6f}, {x:.6f}] (точний корінь знайдено)")
                break
            elif f_left * f_x < 0:
                right = x
            else:
                left = x

            print(f"Вихідний інтервал [{left:.6f}, {right:.6f}]")

            # Оновлення чисел Фібоначчі
            a_fib, b_fib = b_fib, a_fib + b_fib

        root = (left + right) / 2
        return root, iterations

    roots = []
    iterations_list = []
    for interval in isolation_intervals:
        root, iters = fibonacci_verbose(f, interval[0], interval[1], epsilon)
        roots.append(root)
        iterations_list.append(iters)

    print("\nЗнайдені корені (з точністю ε = {}):".format(epsilon))
    for i, (root, iters) in enumerate(zip(roots, iterations_list), 1):
        print(f"  Корінь {i}: x = {root:.6f}, f(x) = {f(root):.2e}, ітерацій: {iters}")

def method_golden_section():
    global coefficients, a, b, epsilon

    if not coefficients or a is None or b is None or epsilon is None:
        print("Дані не задані. Спочатку введіть усі необхідні параметри.")
        return

    def f(x):
        return (coefficients[0] * x**3 +
                coefficients[1] * x**2 +
                coefficients[2] * x +
                coefficients[3])

    print("\n=== Метод золотого перетину ===")

    # Крок 1: Ізоляція коренів
    x = a
    isolation_intervals = []
    step = 0.1
    while x + step <= b:
        x1 = x
        x2 = x + step
        if f(x1) * f(x2) < 0:
            isolation_intervals.append((x1, x2))
        x += step

    if not isolation_intervals:
        print("Не знайдено ізольованих інтервалів з коренями.")
        return

    print(f"Знайдено {len(isolation_intervals)} ізольованих інтервалів з можливими коренями:")
    for i, (start, end) in enumerate(isolation_intervals, 1):
        print(f"  Інтервал {i}: [{start:.4f}; {end:.4f}]")

    # Крок 2: Метод золотого перетину
    def golden_section_verbose(f, left, right, eps):
        phi = 0.618  # Золотий коефіцієнт
        iterations = 0

        while abs(right - left) >= 2 * eps:
            iterations += 1
            prev_left, prev_right = left, right

            x = left + phi * (right - left)
            fx = f(x)
            f_left = f(left)

            print(f"  Ітерація {iterations}: Вхідний інтервал [{prev_left:.6f}, {prev_right:.6f}]", end=", ")

            if fx == 0:
                left = right = x
                print(f"Вихідний інтервал: [{x:.6f}, {x:.6f}] (точний корінь знайдено)")
                break
            elif f_left * fx < 0:
                right = x
            else:
                left = x

            print(f"Вихідний інтервал: [{left:.6f}, {right:.6f}]")

        root = (left + right) / 2
        return root, iterations

    roots = []
    iterations_list = []
    for interval in isolation_intervals:
        root, iters = golden_section_verbose(f, interval[0], interval[1], epsilon)
        roots.append(root)
        iterations_list.append(iters)

    print("\nЗнайдені корені (з точністю ε = {}):".format(epsilon))
    for i, (root, iters) in enumerate(zip(roots, iterations_list), 1):
        print(f"  Корінь {i}: x = {root:.6f}, f(x) = {f(root):.2e}, ітерацій: {iters}")


if __name__ == "__main__":
    main()
