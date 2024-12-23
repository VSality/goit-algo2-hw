def find_min_max(arr):

    def divide_and_conquer(start, end):
        # Базовий випадок: якщо масив має лише один елемент
        if start == end:
            return arr[start], arr[start]

        # Базовий випадок: якщо масив має два елементи
        if end - start == 1:
            return min(arr[start], arr[end]), max(arr[start], arr[end])

        # Розділення масиву на дві частини
        mid = (start + end) // 2
        min1, max1 = divide_and_conquer(start, mid)
        min2, max2 = divide_and_conquer(mid + 1, end)

        return min(min1, min2), max(max1, max2)

    return divide_and_conquer(0, len(arr) - 1)


arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(find_min_max(arr))
