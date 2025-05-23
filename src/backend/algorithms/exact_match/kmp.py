from .exact_string_matching_algorithm import ExactStringMatchingAlgorithm


class KMP(ExactStringMatchingAlgorithm):
    def __init__(self):
        pass

    def _compute_lps_array(self, pattern: str) -> list[int]:
        """
        Helper for KMP: Computes the Longest Proper Prefix which is also Suffix (LPS) array.
        """
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    def search(self, text: str, pattern: str) -> list[int]:
        """
        Implements the Knuth-Morris-Pratt (KMP) string searching algorithm.
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

        lps = self._compute_lps_array(pattern)
        i = 0
        j = 0
        occurrences = []

        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            if j == m:
                occurrences.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return occurrences
