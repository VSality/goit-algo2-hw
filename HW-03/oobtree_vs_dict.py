import csv
import timeit
import os
from BTrees.OOBTree import OOBTree

# Завантаження даних
def load_data(file_path):
    items = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                'ID': int(row['ID']),
                'Name': row['Name'],
                'Category': row['Category'],
                'Price': float(row['Price'])
            }
            items.append(item)
    return items

# Додавання товарів до OOBTree
def add_item_to_tree(tree, item):
    tree[item['ID']] = item

# Додавання товарів до dict
def add_item_to_dict(dictionary, item):
    dictionary[item['ID']] = item

# Діапазонний запит для OOBTree
def range_query_tree(tree, min_price, max_price):
    return [item for item in tree.items(min_price, max_price) if min_price <= item[1]['Price'] <= max_price]

# Діапазонний запит для dict
def range_query_dict(dictionary, min_price, max_price):
    return [item for item in dictionary.values() if min_price <= item['Price'] <= max_price]

# Вимірювання часу виконання
def measure_time(func, *args):
    return timeit.timeit(lambda: func(*args), number=100)

# Основна програма
def main():
    file_path = os.path.join(os.path.dirname(__file__), "generated_items_data.csv")
    data = load_data(file_path)

    # Для OOBTree
    tree = OOBTree()
    for item in data:
        add_item_to_tree(tree, item)
    
    range_query_time_tree = measure_time(range_query_tree, tree, 50, 150)
    print(f"Total range_query time for OOBTree: {range_query_time_tree} seconds")

    # Для dict
    dictionary = {}
    for item in data:
        add_item_to_dict(dictionary, item)
    
    range_query_time_dict = measure_time(range_query_dict, dictionary, 50, 150)
    print(f"Total range_query time for Dict: {range_query_time_dict} seconds")

if __name__ == "__main__":
    main()
