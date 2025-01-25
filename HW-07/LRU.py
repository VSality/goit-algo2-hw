import random
import time
from functools import lru_cache

# Глобальний масив
data = [random.randint(1, 100) for _ in range(100_000)]

# Реалізація функцій без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value


# Реалізація функцій з кешем
@lru_cache(maxsize=1000)
def cached_range_sum(L, R):
    return sum(data[L:R+1])

def range_sum_with_cache(array, L, R):
    return cached_range_sum(L, R)

def update_with_cache(array, index, value):
    global data
    data[index] = value
    cached_range_sum.cache_clear()  # Очищуємо кеш


def main():
    queries = []
    for _ in range(50_000):
        if random.choice(['Range', 'Update']) == 'Range':
            L = random.randint(0, 99_999)
            R = random.randint(L, 99_999)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, 99_999)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))

    # Тестування без кешу
    start = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(data, query[1], query[2])
        elif query[0] == 'Update':
            update_no_cache(data, query[1], query[2])
    no_cache_time = time.time() - start

    # Тестування з кешем
    start = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(data, query[1], query[2])
        elif query[0] == 'Update':
            update_with_cache(data, query[1], query[2])
    with_cache_time = time.time() - start

    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {with_cache_time:.2f} секунд")

if __name__ == "__main__":
    main()
