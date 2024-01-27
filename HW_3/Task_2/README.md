# Завдання 2 (Друга частина для процесів)

Напишіть реалізацію функції factorize, яка приймає список чисел та повертає список чисел, на які числа з вхідного списку поділяються без залишку.

Реалізуйте синхронну версію та виміряйте час виконання.

Потім покращіть продуктивність вашої функції, реалізувавши використання кількох ядер процесора для паралельних обчислень і замірьте час виконання знову. Для визначення кількості ядер на машині використовуйте функцію cpu_count() з пакета multiprocessing

Для перевірки правильності роботи алгоритму самої функції можете скористатися тестом:
```
def factorize(*number):
    # YOUR CODE HERE
    raise NotImplementedError() # Remove after implementation


a, b, c, d  = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
```

## Результат виконання програми
```
Execution time of synchronous version: 0.341197 seconds
Execution time of parallel computing: 0.438667 seconds
```