from typing import List


class TrieNode:
    def __init__(self, val: str = None) -> None:
        self.val = val
        self.children = {}
        self.is_end = False
        self.suggestions = []


class Autocomplete:
    NUMBER_OF_SUGGESTIONS = 4

    def __init__(self):
        self.trie = TrieNode()

    def add_word(self, word: str) -> None:
        """
        Adds a word into the trie. It ignores cases.
        """
        node = self.trie
        for c in word:
            c = c.casefold()  # Case fold: Lower case, but works with Unicode as well.
            if c not in node.children:
                node.children[c] = TrieNode(c)
            node = node.children[c]
        # Mark the existence of a word in this node.
        node.is_end = True

    def populate(self, keywords: List[str]) -> None:
        """
        Populates the trie with the provided list of words.
        """
        for word in keywords:
            self.add_word(word)

    def get_suggestions(self, prefix: str) -> List[str]:
        """
        Offer up to NUMBER_OF_SUGGESTIONS suggestions from the trie, starting with the provided prefix.
        """
        if not prefix:
            return []

        def dfs(node: TrieNode, characters: List[str]) -> None:
            """
            A helper function that runs a DFS on the trie, starting with the given prefix, and adds up to
             NUMBER_OF_SUGGESTIONS words to the suggestions list.
            """
            if len(suggestions) == self.NUMBER_OF_SUGGESTIONS:
                return None
            # If a word is found.
            if node.is_end:
                suggestions.append(''.join(characters))
            for c in sorted(node.children.keys()):
                dfs(node.children[c], characters + [c])

        node = self.trie
        suggestions = []
        # Move the current node to the end of the prefix.
        for c in prefix:
            if c not in node.children:
                return suggestions
            node = node.children[c]
        # If we have not computed suggestions for this node yet.
        if not node.suggestions:
            # Search for valid words.
            dfs(node, list(prefix))
            node.suggestions = suggestions
        return node.suggestions
