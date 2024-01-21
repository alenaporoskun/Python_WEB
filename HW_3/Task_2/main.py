import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

def main():
    # Реалізуємо синхронну версію та виміряємо час виконання

    start_time = time.time()
    a, b, c, d  = factorize(128, 255, 99999, 10651060)
    end_time = time.time()

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    execution_time = end_time - start_time
    print(f"Execution time of synchronous version: {execution_time:.6f} seconds")

    # Використовуємо кілька ядер процесора для паралельних обчислень і заміримо час виконання знову

    start_time2 = time.time()

    a, b, c, d = factorize_parallel(128, 255, 99999, 10651060)

    end_time2 = time.time()

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    execution_time2 = end_time2 - start_time2
    print(f"Execution time of parallel computing: {execution_time2:.6f} seconds")


def factorize(*numbers):
    '''
    Функція приймає список чисел та повертає список чисел, на які числа з вхідного 
    списку поділяються без залишку.
    '''
    result = []
    for num in numbers:
        dividers = []
        for i in range(1, num + 1):
            if num % i == 0:
                dividers.append(i)
        result.append(dividers)
    return result

def factorize_single(num):
    '''
    Функція приймає число та повертає список чисел, на які числа поділяються 
    без залишку.
    '''
    result = []
    for i in range(1, num + 1):
        if num % i == 0:
            result.append(i)
    return result

def factorize_parallel(*numbers):
    # Запускаємо паралельні обчислення з використанням ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        # Використовуємо map для виклику factorize_single для кожного числа у numbers
        result = list(executor.map(factorize_single, numbers))
    return result

if __name__ == "__main__":
    main()