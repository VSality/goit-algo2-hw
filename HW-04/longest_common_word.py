from trie1 import Trie

class LongestCommonWord(Trie):

    def find_longest_common_word(self, strings) -> str:
        if not isinstance(strings, list) or any(not isinstance(s, str) for s in strings):
            raise ValueError("Input must be a list of strings.")
        
        if not strings:
            return ""

        # Вставка слів у Trie
        for word in strings:
            self.put(word, None)

        # Пошук найдовшого спільного префікса
        prefix = []
        node = self.root
        while len(node.children) == 1 and node.value is None:
            char, next_node = next(iter(node.children.items()))
            prefix.append(char)
            node = next_node

        return "".join(prefix)

if __name__ == "__main__":
    # Тести
    trie = LongestCommonWord()
    strings = ["flower", "flow", "flight"]
    assert trie.find_longest_common_word(strings) == "fl"

    trie = LongestCommonWord()
    strings = ["interspecies", "interstellar", "interstate"]
    assert trie.find_longest_common_word(strings) == "inters"

    trie = LongestCommonWord()
    strings = ["dog", "racecar", "car"]
    assert trie.find_longest_common_word(strings) == ""

    print("All tests passed!")
