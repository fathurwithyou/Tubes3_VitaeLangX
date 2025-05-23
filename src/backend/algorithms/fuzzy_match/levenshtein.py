from .string_similarity_algorithm import StringSimilarityAlgorithm


class Levenshtein(StringSimilarityAlgorithm):
    """
    Implements the Levenshtein distance algorithm for string similarity.
    """

    def __init__(self):
        pass

    def calculate_similarity_percentage(self, s1: str, s2: str) -> float:
        """
        Calculates similarity percentage based on Levenshtein distance.
        """
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 100.0
        distance = self.calculate_distance(s1, s2)
        return (1 - (distance / max_len)) * 100

    def calculate_distance(self, s1: str, s2: str) -> int:
        """
        Computes the Levenshtein distance between two strings.
        """
        if len(s1) < len(s2):
            return self.calculate_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
