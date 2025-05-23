from abc import ABC, abstractmethod


class BaseSearchAlgorithm(ABC):
    """
    Kelas dasar abstrak generik untuk semua jenis algoritma pencarian.
    Ini bisa menjadi induk dari kelas dasar yang lebih spesifik.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def search(self, text: str, pattern: any) -> any:
        """
        Metode pencarian umum. Tipe 'pattern' dan 'return' bisa lebih spesifik
        di kelas turunan.
        """
        pass
