from trie1 import Trie

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise ValueError("Pattern must be a string.")

        def dfs(node, current_word):
            count = 0
            # Перевіряємо, чи слово утворене з вузлів закінчується на суфікс
            if node.value is not None and current_word.endswith(pattern):
                count += 1
            for char, child in node.children.items():
                count += dfs(child, current_word + char)
            return count

        count = 0
        for char, child in self.root.children.items():
            count += dfs(child, char)
        return count


    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise ValueError("Prefix must be a string.")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True

if __name__ == "__main__":
    tries = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        tries.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert tries.count_words_with_suffix("e") == 1  # apple
    assert tries.count_words_with_suffix("ion") == 1  # application
    assert tries.count_words_with_suffix("a") == 1  # banana
    assert tries.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert tries.has_prefix("app") == True  # apple, application
    assert tries.has_prefix("bat") == False
    assert tries.has_prefix("ban") == True  # banana
    assert tries.has_prefix("ca") == True  # cat

    print("All tests passed!")
