from .multi_pattern_string_matching import MultiPatternStringMatchingAlgorithm
from collections import deque


class AhoCorasick(MultiPatternStringMatchingAlgorithm):
    """
    Implementasi algoritma Aho-Corasick untuk pencocokan multi-pola string.
    """

    def __init__(self):
        super().__init__()
        self._nodes = []
        self._pattern_map = {}

        self._automaton_built_for_patterns = None
        self._initialize_automaton()

    def _initialize_automaton(self):
        """Menginisialisasi atau mereset struktur otomaton."""

        self._nodes = [{'children': {}, 'parent': None,
                        'char': None, 'failure_link': 0, 'output': set()}]
        self._pattern_map = {}
        self._automaton_built_for_patterns = None

    def _build_automaton(self, patterns: list[str]):
        """
        Membangun Trie (fungsi goto), fungsi failure, dan fungsi output
        untuk daftar pola yang diberikan.
        """
        self._initialize_automaton()

        valid_patterns = [p for p in patterns if p]
        if not valid_patterns:
            self._automaton_built_for_patterns = tuple(
                sorted(patterns))
            return

        self._pattern_map = {i: pattern_str for i,
                             pattern_str in enumerate(valid_patterns)}

        for pattern_idx, pattern_str in self._pattern_map.items():
            node_idx = 0
            for char_in_pattern in pattern_str:
                if char_in_pattern not in self._nodes[node_idx]['children']:

                    new_node_idx = len(self._nodes)
                    self._nodes[node_idx]['children'][char_in_pattern] = new_node_idx
                    self._nodes.append({
                        'children': {},
                        'parent': node_idx,
                        'char': char_in_pattern,
                        'failure_link': 0,
                        'output': set()
                    })
                node_idx = self._nodes[node_idx]['children'][char_in_pattern]

            self._nodes[node_idx]['output'].add(pattern_idx)

        queue = deque()

        for child_node_idx in self._nodes[0]['children'].values():

            queue.append(child_node_idx)

        while queue:
            current_node_idx = queue.popleft()
            for char, next_node_idx in self._nodes[current_node_idx]['children'].items():
                queue.append(next_node_idx)

                failure_candidate_idx = self._nodes[current_node_idx]['failure_link']
                while char not in self._nodes[failure_candidate_idx]['children'] and failure_candidate_idx != 0:
                    failure_candidate_idx = self._nodes[failure_candidate_idx]['failure_link']

                if char in self._nodes[failure_candidate_idx]['children']:
                    self._nodes[next_node_idx]['failure_link'] = self._nodes[failure_candidate_idx]['children'][char]
                else:

                    pass

                output_from_failure = self._nodes[self._nodes[next_node_idx]
                                                  ['failure_link']]['output']
                if output_from_failure:
                    self._nodes[next_node_idx]['output'].update(
                        output_from_failure)

        self._automaton_built_for_patterns = tuple(sorted(patterns))

    def search(self, text: str, patterns: list[str]) -> dict[str, list[int]]:
        """
        Mencari semua kemunculan dari daftar 'patterns' dalam 'text'
        menggunakan algoritma Aho-Corasick.

        Args:
            text (str): Teks tempat pencarian dilakukan.
            patterns (list[str]): Daftar pola string yang akan dicari.

        Returns:
            dict[str, list[int]]: Dictionary dengan key adalah string pola yang ditemukan
                                   dan value adalah list berisi indeks awal kemunculannya di teks.
        """
        if not text or not patterns:
            return {}

        current_patterns_tuple = tuple(
            sorted(p for p in patterns if p))

        if not current_patterns_tuple:
            return {}

        if self._automaton_built_for_patterns != current_patterns_tuple:

            self._build_automaton([p for p in patterns if p])

        if len(self._nodes) <= 1 and not self._nodes[0]['children']:
            return {}

        results = {self._pattern_map[idx]: [] for idx in self._pattern_map}
        current_node_idx = 0

        for i, char_in_text in enumerate(text):

            while char_in_text not in self._nodes[current_node_idx]['children'] and current_node_idx != 0:
                current_node_idx = self._nodes[current_node_idx]['failure_link']

            if char_in_text in self._nodes[current_node_idx]['children']:
                current_node_idx = self._nodes[current_node_idx]['children'][char_in_text]
            else:
                pass

            if self._nodes[current_node_idx]['output']:
                for pattern_idx in self._nodes[current_node_idx]['output']:
                    matched_pattern_str = self._pattern_map[pattern_idx]

                    start_index = i - len(matched_pattern_str) + 1
                    results[matched_pattern_str].append(start_index)

        final_results = {}
        for pattern_str, indices in results.items():
            if indices:
                final_results[pattern_str] = sorted(list(set(indices)))

        return final_results
