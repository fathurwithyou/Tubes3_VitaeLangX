from ..base_search_algorithm import BaseSearchAlgorithm
from abc import abstractmethod


class ExactStringMatchingAlgorithm(BaseSearchAlgorithm):
    """
    Kelas dasar abstrak untuk algoritma pencocokan string eksak.
    Algoritma turunan akan mencari semua kemunculan sebuah 'pattern' string
    di dalam sebuah 'text' string.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def search(self, text: str, pattern: str) -> list[int]:
        """
        Metode abstrak untuk mencari semua kemunculan pattern (string) dalam text (string).

        Args:
            text (str): Teks tempat pencarian dilakukan.
            pattern (str): Pola string yang dicari.

        Returns:
            list[int]: Daftar indeks awal (0-based) di mana pattern ditemukan dalam text.
                       Mengembalikan list kosong jika tidak ada kemunculan yang ditemukan.
        """
        pass
