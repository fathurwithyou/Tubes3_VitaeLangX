from .exact_string_matching_algorithm import ExactStringMatchingAlgorithm

class BoyerMoore(ExactStringMatchingAlgorithm):
    def __init__(self):
        pass

    def _bad_char_heuristic(self, pattern: str) -> dict[str, int]:
        """
        Helper for Boyer-Moore: Computes the bad character shift table.
        For each character, stores the rightmost position in the pattern.
        """
        m = len(pattern)
        bad_char = {}

        for i in range(m):
            bad_char[pattern[i]] = i

        return bad_char

    def search(self, text: str, pattern: str) -> list[int]:
        """
        Implements the Boyer-Moore string searching algorithm (simplified for bad character heuristic).
        Returns a list of starting indices where the pattern is found in the text.
        """
        n = len(text)
        m = len(pattern)
        if m == 0:
            return []
        if n == 0:
            return []
        if m > n:
            return []

        bad_char = self._bad_char_heuristic(pattern)
        occurrences = []
        s = 0

        while s <= (n - m):
            j = m - 1
            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1

            if j < 0:
                occurrences.append(s)
                if s + m < n:
                    next_char = text[s + m]
                    if next_char in bad_char:
                        shift = m - bad_char[next_char] - 1
                    else:
                        shift = m
                    s += max(1, shift)
                else:
                    s += 1
            else:
                mismatched_char = text[s + j]
                if mismatched_char in bad_char:
                    shift = j - bad_char[mismatched_char]
                else:
                    shift = j + 1
                s += max(1, shift)

        return occurrences
