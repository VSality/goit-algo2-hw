import random
from typing import Dict
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1): 
        self.window_size = window_size
        self.max_requests = max_requests
        # Словник для зберігання історії повідомлень для кожного користувача
        self.users_history: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        history = self.users_history.get(user_id, deque())
        while history and history[0] < current_time - self.window_size:
            history.popleft()
        self.users_history[user_id] = history

    def can_send_message(self, user_id: str) -> bool: # Перевіряємо, чи можна відправити нове повідомлення
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        return len(self.users_history.get(user_id, deque())) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        # Якщо користувач може відправити повідомлення
        if len(self.users_history.get(user_id, deque())) < self.max_requests:
            # Додаємо повідомлення до історії
            if user_id not in self.users_history:
                self.users_history[user_id] = deque()
            self.users_history[user_id].append(current_time)
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        history = self.users_history.get(user_id, deque())
        # Якщо користувач не має повідомлень, можна відправляти
        if not history:
            return 0.0
        # Якщо повідомлення вже є, чекаємо наступне доступне вікно
        next_allowed_time = history[0] + self.window_size
        return max(0.0, next_allowed_time - current_time)

# Демонстрація роботи
def test_rate_limiter():
    # Створюємо rate limiter: вікно 10 секунд, 1 повідомлення
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Симулюємо потік повідомлень від користувачів (послідовні ID від 1 до 20)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, 11):
        # Симулюємо різних користувачів (ID від 1 до 5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Невелика затримка між повідомленнями для реалістичності
        # Випадкова затримка від 0.1 до 1 секунди
        time.sleep(random.uniform(0.1, 1.0))

    # Чекаємо, поки вікно очиститься
    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        # Випадкова затримка від 0.1 до 1 секунди
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_rate_limiter()
