import time
from typing import Dict
import random

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0): # Мінімальний інтервал між повідомленнями
        self.min_interval = min_interval
        self.users_last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool: # Перевірка, чи можна відправити повідомлення (чи минув інтервал)
        current_time = time.time()
        last_message_time = self.users_last_message_time.get(user_id)
        if last_message_time is None or current_time - last_message_time >= self.min_interval:
            return True
        return False

    def record_message(self, user_id: str) -> bool:
        current_time = time.time()
        if self.can_send_message(user_id):
            self.users_last_message_time[user_id] = current_time
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        # Якщо повідомлень ще не було, можна відправляти відразу
        last_message_time = self.users_last_message_time.get(user_id)
        if last_message_time is None:
            return 0.0
        # Якщо повідомлення є, обчислюємо час до наступного дозволеного
        next_allowed_time = last_message_time + self.min_interval
        return max(0.0, next_allowed_time - current_time)

def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Випадкова затримка між повідомленнями
        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 10 секунд...")
    time.sleep(10)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_throttling_limiter()
