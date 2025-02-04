import random
import time
import matplotlib.pyplot as plt

def randomized_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return randomized_quick_sort(left) + middle + randomized_quick_sort(right)

def deterministic_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]  # Вибір опорного елемента (середній елемент)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return deterministic_quick_sort(left) + middle + deterministic_quick_sort(right)

def measure_time(sort_function, arr, repetitions=5):
    times = []
    for _ in range(repetitions):
        arr_copy = arr[:]
        start_time = time.time()
        sort_function(arr_copy)
        times.append(time.time() - start_time)
    return sum(times) / repetitions

def main():
    sizes = [10_000, 50_000, 100_000, 500_000]
    rand_times = []
    det_times = []
    
    for size in sizes:
        arr = [random.randint(0, 1_000_000) for _ in range(size)]
        print(f"Розмір масиву: {size}")
        rand_time = measure_time(randomized_quick_sort, arr)
        det_time = measure_time(deterministic_quick_sort, arr)
        rand_times.append(rand_time)
        det_times.append(det_time)
        print(f"Рандомізований QuickSort: {rand_time:.5f} секунд")
        print(f"Детермінований QuickSort: {det_time:.5f} секунд")
        print("-")
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, rand_times, marker='o', linestyle='-', label='Рандомізований QuickSort')
    plt.plot(sizes, det_times, marker='s', linestyle='-', label='Детермінований QuickSort')
    plt.xlabel('Розмір масиву')
    plt.ylabel('Середній час виконання (секунди)')
    plt.title('Порівняння рандомізованого та детермінованого QuickSort')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
