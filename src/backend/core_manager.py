import os
from backend.database_manager import DatabaseManager
from backend.cv_processor import CVProcessor
from backend.search_algorithms import SearchAlgorithms
from backend.regex_extractor import RegexExtractor
from backend.models import ApplicantProfile, ApplicationDetail
from backend.utils import Utils
import re


class BackendManager:
    """
    Orchestrates all backend operations for the ATS.
    Manages database, CV processing, search algorithms, and regex extraction.
    """

    def __init__(self, db_host='localhost', db_user='root', db_password='', db_name='ats_db'):
        self.db_manager = DatabaseManager(
            host=db_host, user=db_user, password=db_password, db=db_name)
        self.cv_processor = CVProcessor()
        self.search_algos = SearchAlgorithms()
        self.regex_extractor = RegexExtractor()
        self.in_memory_cv_texts = {}
        self.applicant_profiles_cache = {}

    def initialize_backend(self, data_directory: str = 'data/'):
        """Initializes database, creates tables, and seeds data if necessary."""
        self.db_manager.connect()
        self.db_manager.create_tables()
        if not self.db_manager.get_all_application_details():
            self.db_manager.seed_data(data_directory)
        self.load_cv_data_to_memory()

    def load_cv_data_to_memory(self):
        """
        Loads all relevant CV texts into memory for efficient searching. [cite: 16, 25]
        This should happen once on application startup or when new CVs are added.
        """
        application_details = self.db_manager.get_all_application_details()
        cv_paths = [
            detail.cv_path for detail in application_details if detail.cv_path]
        print(f"Loading {len(cv_paths)} CVs into memory...")
        self.in_memory_cv_texts = self.cv_processor.process_cv_for_pattern_matching(
            cv_paths)
        print("All relevant CV data loaded into memory.")

    def search_cvs(self, keywords: list[str], algorithm: str, top_n_matches: int = 10, fuzzy_threshold: float = None) -> dict:
        """
        Performs CV search based on keywords using the specified algorithm.
        Returns structured results including exact and fuzzy matches.
        """
        results = []
        exact_match_time = 0
        fuzzy_match_time = 0

        keywords_lower = [k.lower() for k in keywords]

        exact_matches = {}
        print(
            f"Starting exact matching with {algorithm} for keywords: {keywords}")
        exact_search_func = self.search_algos.kmp_search if algorithm.lower(
        ) == 'kmp' else self.search_algos.boyer_moore_search
        if algorithm.lower() == 'aho-corasick':

            multi_pattern_results, exact_match_time = Utils.time_function(
                self.search_algos.aho_corasick_search,

                list(self.in_memory_cv_texts.values())[
                    0] if self.in_memory_cv_texts else "",
                keywords_lower
            )

            for cv_path, text in self.in_memory_cv_texts.items():
                cv_matched_keywords = {}
                total_occurrences = 0
                for keyword in keywords_lower:

                    occurrences = exact_search_func(text.lower(), keyword)
                    if occurrences:
                        cv_matched_keywords[keyword] = len(occurrences)
                        total_occurrences += len(occurrences)
                if total_occurrences > 0:
                    exact_matches[cv_path] = {
                        'matched_keywords': cv_matched_keywords,
                        'total_occurrences': total_occurrences
                    }
        else:
            for cv_path, text in self.in_memory_cv_texts.items():
                cv_matched_keywords = {}
                total_occurrences = 0

                current_cv_exact_matches = {}
                current_cv_exact_time = 0

                for keyword in keywords_lower:
                    occurrences, time_taken = Utils.time_function(

                        exact_search_func, text.lower(), keyword)
                    current_cv_exact_time += time_taken
                    if occurrences:
                        current_cv_exact_matches[keyword] = len(occurrences)
                        total_occurrences += len(occurrences)

                if total_occurrences > 0:
                    exact_matches[cv_path] = {
                        'matched_keywords': current_cv_exact_matches,
                        'total_occurrences': total_occurrences
                    }
                exact_match_time += current_cv_exact_time

        sorted_exact_matches = sorted(exact_matches.items(
        ), key=lambda item: item[1]['total_occurrences'], reverse=True)

        unmatched_keywords = []
        for keyword in keywords:
            if not any(keyword.lower() in details['matched_keywords'] for cv_path, details in sorted_exact_matches):
                unmatched_keywords.append(keyword)

        fuzzy_matches = {}
        print(
            f"Starting fuzzy matching for unmatched keywords: {unmatched_keywords}")

        if unmatched_keywords and fuzzy_threshold is not None:
            for cv_path, text in self.in_memory_cv_texts.items():
                cv_fuzzy_keywords = {}
                highest_cv_similarity = 0.0

                current_cv_fuzzy_matches = {}
                current_cv_fuzzy_time = 0

                cv_words = re.findall(r'\b\w+\b', text.lower())

                for um_keyword in unmatched_keywords:
                    best_similarity = 0.0
                    for cv_word in cv_words:
                        similarity_score, time_taken = Utils.time_function(
                            self.search_algos.calculate_similarity_percentage, um_keyword.lower(), cv_word)
                        current_cv_fuzzy_time += time_taken
                        if similarity_score >= fuzzy_threshold and similarity_score > best_similarity:
                            best_similarity = similarity_score
                    if best_similarity > 0:
                        cv_fuzzy_keywords[um_keyword] = best_similarity
                        if best_similarity > highest_cv_similarity:
                            highest_cv_similarity = best_similarity

                if highest_cv_similarity > 0:
                    fuzzy_matches[cv_path] = {
                        'fuzzy_matched_keywords': cv_fuzzy_keywords,
                        'highest_similarity': highest_cv_similarity
                    }
                fuzzy_match_time += current_cv_fuzzy_time

        final_results = []
        processed_cv_paths = set()

        for cv_path, details in sorted_exact_matches:

            application_detail = self.db_manager.get_all_application_details()
            app_detail = next(
                (ad for ad in application_detail if ad.cv_path == cv_path), None)

            if app_detail:
                profile = self.db_manager.get_applicant_profile_by_id(
                    app_detail.applicant_id)
                if profile:
                    results.append({
                        'applicant_id': profile.applicant_id,
                        'name': f"{profile.first_name} {profile.last_name}".strip(),
                        'cv_path': cv_path,
                        'matched_keywords': details['matched_keywords'],
                        'total_occurrences': details['total_occurrences'],
                        'fuzzy_keywords': {},
                        'highest_fuzzy_similarity': 0.0
                    })
                    processed_cv_paths.add(cv_path)

        sorted_fuzzy_matches = sorted(fuzzy_matches.items(
        ), key=lambda item: item[1]['highest_similarity'], reverse=True)

        for cv_path, details in sorted_fuzzy_matches:
            if cv_path not in processed_cv_paths:
                application_detail = self.db_manager.get_all_application_details()
                app_detail = next(
                    (ad for ad in application_detail if ad.cv_path == cv_path), None)
                if app_detail:
                    profile = self.db_manager.get_applicant_profile_by_id(
                        app_detail.applicant_id)
                    if profile:
                        results.append({
                            'applicant_id': profile.applicant_id,
                            'name': f"{profile.first_name} {profile.last_name}".strip(),
                            'cv_path': cv_path,
                            'matched_keywords': {},
                            'total_occurrences': 0,
                            'fuzzy_keywords': details['fuzzy_matched_keywords'],
                            'highest_fuzzy_similarity': details['highest_similarity']
                        })
                        processed_cv_paths.add(cv_path)

        final_results = results[:top_n_matches]

        return {
            "results": final_results,
            "exact_match_time_ms": exact_match_time,
            "fuzzy_match_time_ms": fuzzy_match_time if unmatched_keywords else 0
        }

    def get_cv_summary(self, applicant_id: int) -> dict:
        """
        Extracts and returns a detailed summary of a CV for a given applicant ID. [cite: 75, 77, 78]
        This involves fetching the CV path, extracting text, and applying Regex.
        """
        profile = self.db_manager.get_applicant_profile_by_id(applicant_id)
        if not profile:
            return {"error": "Applicant not found."}

        application_details = self.db_manager._execute_query(
            "SELECT * FROM ApplicationDetail WHERE applicant_id = %s ORDER BY detail_id DESC LIMIT 1",
            (applicant_id,), fetch_one=True
        )
        if not application_details:
            return {"error": "CV details not found for this applicant."}

        cv_path = application_details['cv_path']
        if not cv_path or not os.path.exists(cv_path):
            return {"error": f"CV file not found at {cv_path}"}

        cv_text = self.cv_processor.extract_text_from_pdf(cv_path)
        if not cv_text:
            return {"error": "Could not extract text from CV."}

        summary = {
            "applicant_info": {
                "name": f"{profile.first_name} {profile.last_name}".strip(),

                "birthdate": str(profile.date_of_birth) if profile.date_of_birth else "N/A",
                "address": profile.address,
                "phone_number": profile.phone_number,
            },
            "extracted_info": {
                "summary_text": self.regex_extractor.extract_summary(cv_text),
                "skills": self.regex_extractor.extract_skills(cv_text),
                "job_history": self.regex_extractor.extract_job_history(cv_text),
                "education": self.regex_extractor.extract_education(cv_text)
            }
        }
        return summary

    def get_raw_cv_path(self, applicant_id: int) -> str:
        """Returns the path to the raw CV file for viewing."""
        application_details = self.db_manager._execute_query(
            "SELECT cv_path FROM ApplicationDetail WHERE applicant_id = %s ORDER BY detail_id DESC LIMIT 1",
            (applicant_id,), fetch_one=True
        )
        if application_details:
            return application_details['cv_path']
        return None

    def shutdown_backend(self):
        """Closes any open connections."""
        self.db_manager.close()
