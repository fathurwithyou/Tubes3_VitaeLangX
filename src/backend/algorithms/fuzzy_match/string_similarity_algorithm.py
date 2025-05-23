# import abc
from abc import ABC, abstractmethod


class StringSimilarityAlgorithm(ABC):
    """
    Kelas dasar abstrak untuk algoritma yang mengukur kemiripan antar string.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_distance(self, s1: str, s2: str) -> int | float:
        """
        Menghitung jarak atau ketidakmiripan antara dua string.
        Nilai yang lebih rendah biasanya berarti lebih mirip.

        Args:
            s1 (str): String pertama.
            s2 (str): String kedua.

        Returns:
            int | float: Nilai jarak antar string.
        """
        pass

    @abstractmethod
    def calculate_similarity_percentage(self, s1: str, s2: str) -> float:
        """
        Menghitung persentase kemiripan antara dua string.
        Nilai berkisar antara 0.0 hingga 100.0.

        Args:
            s1 (str): String pertama.
            s2 (str): String kedua.

        Returns:
            float: Persentase kemiripan.
        """
        pass
