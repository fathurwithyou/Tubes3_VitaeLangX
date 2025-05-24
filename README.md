# Applicant Tracking System (ATS)

![Python Version](https://img.shields.io/badge/Python-3.13-blue?style=plastic&logo=python)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange?style=plastic&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green?style=plastic)

This project implements a backend for an Applicant Tracking System, focusing on efficient CV processing and keyword searching using various string matching algorithms.

## Features

* **CV Text Extraction**: Extracts text content from PDF CVs.
* **Information Extraction**: Uses regular expressions to extract summaries, skills, job history, and education from CV text.
* **Advanced Search Algorithms**: Implements and utilizes string matching algorithms for efficient keyword searching:
    * **Knuth-Morris-Pratt (KMP)**: An exact string matching algorithm that efficiently finds occurrences of a "pattern" string within a "text" string. It optimizes by avoiding re-matching characters that are already known to match based on prefixes and suffixes of the pattern.
    * **Boyer-Moore (BM)**: An exact string matching algorithm that typically performs fewer comparisons than KMP, especially on longer patterns. It works by comparing the pattern from right to left and uses a "bad character heuristic" to determine how far to shift the pattern when a mismatch occurs.
    * **Aho-Corasick**: A multi-pattern string matching algorithm that finds all occurrences of a set of patterns within a text. It builds a Trie-like structure with "failure links" and "output functions" to achieve efficient simultaneous searching.
    * **Levenshtein Distance**: A fuzzy matching algorithm that calculates the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word into the other. It's used to determine the similarity percentage between two strings.

## Requirements and Installation


### Prerequisites

* **Python 3.13 or higher**: Ensure you have Python version 3.13 or a newer version installed on your system.
* **MySQL Server**: A running MySQL server instance is required. By default, the application attempts to connect using `root` as the username and an empty password. If your MySQL configuration differs, you will need to modify the `BackendManager` initialization call by providing the appropriate `db_host`, `db_user`, `db_password`, and `db_name` parameters.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd src
    ```

2.  **Install `uv` (a fast Python package installer and runner):**

    ```bash
    pip install uv
    ```

3.  **Install Python dependencies using `uv`:**

    ```bash
    uv pip install -r requirements.txt
    ```

## Building and Running the Program

1.  **Seed the database:** This step will connect to your MySQL server, create the necessary database and tables (if they don't exist), and populate the `ApplicationDetail` table with CV paths from the `data` directory. It uses a default applicant profile for all entries.

    ```bash
    uv run seed.py
    ```

2.  **Run the main application:** This will initialize the backend, load CV data into memory, and demonstrate search functionalities.

    ```bash
    uv run main.py
    ```

## Tree
alias pytree='LC_COLLATE=C tree -I "__pycache__|*.pyc" --sort=name'

## Contributors

| Nama  | NIM |
| :---- | :-- |
| Adinda Putri | 13523071 |
| Muhammad Fathur Rizky | 13523105 |
| Ahmad Wicaksono | 13523121 |