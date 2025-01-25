from functools import lru_cache
import timeit
import matplotlib.pyplot as plt

class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root

        else:
            if root.right is None:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right else root

    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return

        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

def fibonacci_lru(n):
    @lru_cache(maxsize=None)
    def fib_lru_iterative(n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    return fib_lru_iterative(n)

def fibonacci_splay(n, tree):
    cached = tree.search(n)
    if cached is not None:
        return cached

    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)

    tree.insert(n, result)
    return result


def compare_performance():
    numbers = list(range(0, 951, 50))
    lru_times = []
    splay_times = []

    tree = SplayTree()

    for n in numbers:
        # LRU Cache
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10)
        lru_times.append(lru_time / 10)

        # Splay Tree
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10)
        splay_times.append(splay_time / 10)

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(numbers, lru_times, label="LRU Cache", marker="o")
    plt.plot(numbers, splay_times, label="Splay Tree", marker="s")
    plt.xlabel("Числа Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid()
    plt.show()

    # Виведення таблиці
    print("n\tLRU Time Cache (s)\tSplay Tree Time (s)")
    print("-" * 40)
    for i, n in enumerate(numbers):
        print(f"{n}\t{lru_times[i]:.6f}\t\t{(splay_times[i]):.6f}")

if __name__ == "__main__":
    compare_performance()
