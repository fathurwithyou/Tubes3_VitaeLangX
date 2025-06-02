from pdfminer.high_level import extract_text
import os

class CVProcessor:
    """
    Handles the extraction of text from PDF CVs and potential creation of basic CV profiles.
    """
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extracts all text from a given PDF file.
        Returns a single long string containing the entire text content.
        """
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file not found at {pdf_path}")
            return ""
        try:
            print(f"Extracting text from {pdf_path}...")
            text = extract_text(pdf_path)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def process_cv_for_pattern_matching(self, cv_paths: list[str]) -> dict[str, str]:
        """
        Processes a list of CV paths, extracting text for pattern matching.
        Returns a dictionary mapping cv_path to its extracted text content.
        This data will be held in-memory for searching.
        """
        in_memory_cv_texts = {}
        print(
            f"Processing {len(cv_paths)} CVs for in-memory pattern matching...")
        for cv_path in cv_paths:
            text = self.extract_text_from_pdf(cv_path)
            if text:
                in_memory_cv_texts[cv_path] = text
        print("CV text extraction for pattern matching complete.")
        return in_memory_cv_texts