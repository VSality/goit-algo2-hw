import json
import os
import time
import random
import mmh3
import math

class HyperLogLog:
    def __init__(self, p=5):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 5 * self.m / 2  # Поріг для малих значень

    def _get_alpha(self):
        if self.p <= 16:
            return 0.673
        elif self.p == 32:
            return 0.697
        else:
            return 0.7213 / (1 + 1.079 / self.m)

    def add(self, item):
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        return len(bin(w)) - 2 if w > 0 else 32

    def count(self):
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * self.m * self.m / Z
        
        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)
        
        return E

# Завантаження даних
def load_data(file_path):
    ip_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            record = json.loads(line)
            ip_list.append(record["remote_addr"])
    return ip_list


def main():
    file_path = os.path.join(os.path.dirname(__file__), "lms-stage-access.logg")
    ip_list = load_data(file_path)
    
    start_time = time.time()
    unique_ips = set(ip_list)
    end_time = time.time()
    
    start_time_hyper = time.time()
    hll = HyperLogLog(p=14)
    # Додаємо елементи
    for i in range(100000):
        hll.add(random.choice(ip_list))
    
    estimated_cardinality = hll.count()
    
    end_time_hyper = time.time()
    
    print("Результати порівняння:       Точний підрахунок   HyperLogLog")
    
    print(f"Унікальні елементи           {len(unique_ips)}                  {estimated_cardinality}")
    print(f"Час виконання (сек.)         {end_time - start_time:.6f}            {end_time_hyper - start_time_hyper:.6f}")


if __name__ == "__main__":
    main()