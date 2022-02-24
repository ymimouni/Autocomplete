from typing import List, Generator


class TrieNode:
    def __init__(self, val: str = None) -> None:
        self.val = val
        self.children = {}
        self.is_end = False
        self.suggestions = []


def children_suggestions(node: TrieNode) -> Generator[str, None, None]:
    """
    A helper function that traverses the children of a node in alphabetic order, and returns their suggestions.
    """
    for c in sorted(node.children.keys()):
        for s in node.children[c].suggestions:
            yield s


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

        def dfs(node: TrieNode, characters: List[str]) -> None:  # noqa
            """
            A helper function that runs a DFS on the trie, starting with the given prefix, and adds up to
             NUMBER_OF_SUGGESTIONS words to the suggestions list.
            """
            if len(suggestions) == self.NUMBER_OF_SUGGESTIONS:
                return None
            # If a word is found.
            if node.is_end:
                suggestions.append(''.join(characters))
            for c in sorted(node.children.keys()):  # noqa
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

    def precompute_suggestions(self) -> None:
        """
        Precompute up to NUMBER_OF_SUGGESTIONS suggestions from the trie, starting with every possible prefix in the
         trie. Save the results in the suggestions list of the corresponding node.
        """
        def traverse(node: TrieNode, characters: List[str]) -> None:  # noqa
            """
            A helper function that uses post-order traversal of the trie to compute suggestions.
            """
            # Traverse the children of the current node.
            for c in sorted(node.children.keys()):
                traverse(node.children[c], characters + [c])
            # If the current node is the end of a word, add it to suggestions.
            if node.is_end:
                node.suggestions.append(''.join(characters))
            # Compose the list of suggestions of the current word based on those of its children.
            for suggestion in children_suggestions(node):
                node.suggestions.append(suggestion)
                if len(node.suggestions) == self.NUMBER_OF_SUGGESTIONS:
                    break

        node = self.trie
        traverse(node, [])
