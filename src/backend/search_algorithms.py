class SearchAlgorithms:
    """
    Contains implementations of string matching algorithms (KMP, Boyer-Moore)
    and string similarity algorithm (Levenshtein Distance).
    """

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

    def kmp_search(self, text: str, pattern: str) -> list[int]:
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

    def _bad_char_heuristic(self, pattern: str) -> dict[str, int]:
        """
        Helper for Boyer-Moore: Computes the bad character shift table.
        """
        m = len(pattern)
        bad_char = {}
        for i in range(m - 1):
            bad_char[pattern[i]] = m - 1 - i
        return bad_char

    def boyer_moore_search(self, text: str, pattern: str) -> list[int]:
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
                    proposed_shift = m - bad_char.get(text[s + m], m)
                    s += max(1, proposed_shift)
                else:
                    s += 1
            else:
                shift_on_mismatch = j - bad_char.get(text[s + j], -1)
                s += max(1, shift_on_mismatch)
        return occurrences

    def levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculates the Levenshtein distance (edit distance) between two strings.
        """
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (0 if c1 == c2 else 1)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def calculate_similarity_percentage(self, s1: str, s2: str) -> float:
        """
        Calculates similarity percentage based on Levenshtein distance.
        """
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 100.0
        distance = self.levenshtein_distance(s1, s2)
        return (1 - (distance / max_len)) * 100

    def aho_corasick_search(self, text: str, patterns: list[str]) -> dict[str, list[int]]:
        """
        Placeholder for Aho-Corasick algorithm for multi-pattern matching.
        This would be implemented if the bonus is pursued.
        Returns a dictionary where keys are patterns and values are lists of their occurrences.
        """

        results = {}
        for pattern in patterns:

            occurrences = self.kmp_search(text, pattern)
            if occurrences:
                results[pattern] = occurrences
        return results
