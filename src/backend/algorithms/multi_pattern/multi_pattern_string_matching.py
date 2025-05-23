from backend.algorithms.base_search_algorithm import BaseSearchAlgorithm
from abc import abstractmethod


class MultiPatternStringMatchingAlgorithm(BaseSearchAlgorithm):
    """
    Kelas dasar abstrak untuk algoritma pencocokan multi-pola string.
    Algoritma turunan akan mencari semua kemunculan dari beberapa pattern (list of strings)
    di dalam sebuah 'text' string.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def search(self, text: str, patterns: list[str]) -> dict[str, list[int]]:
        """
        Metode abstrak untuk mencari semua kemunculan dari beberapa pattern dalam text.

        Args:
            text (str): Teks tempat pencarian dilakukan.
            patterns (list[str]): Daftar pola string yang dicari.

        Returns:
            dict[str, list[int]]: Dictionary di mana key adalah pattern yang ditemukan
                                   dan value adalah daftar indeks awal kemunculannya.
        """
        pass
