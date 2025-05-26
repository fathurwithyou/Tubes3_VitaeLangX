from backend.algorithms import KMP, BoyerMoore, AhoCorasick, Levenshtein

class SearchService:
    """
    Menyediakan antarmuka terpadu untuk berbagai algoritma pencarian string
    dan perhitungan kemiripan. Menggunakan kelas-kelas algoritma
    yang telah direfaktor.
    """

    def __init__(self):
        """
        Menginisialisasi instance dari algoritma-algoritma pencarian.
        """
        self.kmp_algorithm = KMP()
        self.boyer_moore_algorithm = BoyerMoore()
        self.aho_corasick_algorithm = AhoCorasick()
        self.levenshtein_algorithm = Levenshtein()

    def search_kmp(self, text: str, pattern: str) -> list[int]:
        """
        Melakukan pencarian string eksak menggunakan algoritma KMP.

        Args:
            text (str): Teks utama untuk pencarian.
            pattern (str): Pola yang dicari.

        Returns:
            list[int]: Daftar indeks di mana pola ditemukan.
        """
        return self.kmp_algorithm.search(text, pattern)

    def search_boyer_moore(self, text: str, pattern: str) -> list[int]:
        """
        Melakukan pencarian string eksak menggunakan algoritma Boyer-Moore.

        Args:
            text (str): Teks utama untuk pencarian.
            pattern (str): Pola yang dicari.

        Returns:
            list[int]: Daftar indeks di mana pola ditemukan.
        """
        return self.boyer_moore_algorithm.search(text, pattern)

    def search_aho_corasick(self, text: str, patterns: list[str]) -> dict[str, list[int]]:
        """
        Melakukan pencarian multi-pola menggunakan algoritma Aho-Corasick.

        Args:
            text (str): Teks utama untuk pencarian.
            patterns (list[str]): Daftar pola yang dicari.

        Returns:
            dict[str, list[int]]: Dictionary dengan pola sebagai key dan daftar indeks kemunculan sebagai value.
        """
        return self.aho_corasick_algorithm.search(text, patterns)

    def get_calculate_distance(self, s1: str, s2: str) -> int:
        """
        Menghitung Levenshtein distance antara dua string.
        Wrapper untuk fungsi calculate_distance yang diimpor.

        Args:
            s1 (str): String pertama.
            s2 (str): String kedua.

        Returns:
            int: Jarak Levenshtein.
        """
        return self.levenshtein_algorithm.calculate_distance(s1, s2)

    def get_similarity_percentage(self, s1: str, s2: str) -> float:
        """
        Menghitung persentase kemiripan antara dua string berdasarkan Levenshtein distance.
        Wrapper untuk fungsi calculate_similarity_percentage yang diimpor.

        Args:
            s1 (str): String pertama.
            s2 (str): String kedua.

        Returns:
            float: Persentase kemiripan (0.0 hingga 100.0).
        """
        return self.levenshtein_algorithm.calculate_similarity_percentage(s1, s2)
