
import os
import re
from backend.db import DatabaseManager
from backend.preprocessor import CVProcessor, RegexExtractor
from backend.utils.utils import Utils
from backend.seeder import Seeder
from backend.services import SearchService


class BackendManager:
    """
    Orchestrates all backend operations for the ATS.
    Manages database, CV processing, search algorithms (via SearchService),
    and regex extraction.
    """

    def __init__(self, db_host='localhost', db_user='root', db_password='', db_name='ats_db'):
        self.db_manager = DatabaseManager(
            host=db_host, user=db_user, password=db_password, db=db_name)
        self.cv_processor = CVProcessor()
        self.search_service = SearchService()
        self.regex_extractor = RegexExtractor()
        self.in_memory_cv_texts = {}
        self.applicant_profiles_cache = {}

    def initialize_backend(self, data_directory: str = '../data/'):
        """
        Initializes the application backend.
        Ensures DB connection, table creation, and seeds data via Seeder if necessary.
        """
        print("BackendManager: Initializing backend...")

        self.db_manager.connect()
        if not self.db_manager.connection:
            print(
                "BackendManager: CRITICAL - DB connection failed. Further initialization stopped.")
            return

        self.db_manager.create_tables()

        if not self.db_manager.get_all_application_details():
            print("BackendManager: No application details found. Initiating database preparation and seeding process via Seeder...")
            seeder_instance = Seeder(self.db_manager)
            success = seeder_instance.prepare_database_and_seed(
                data_directory=data_directory)

            if success:
                print(
                    "BackendManager: Seeder successfully prepared database and seeded data.")
            else:
                print(
                    "BackendManager: Seeder reported an issue during database preparation or seeding.")
        else:
            print("BackendManager: Application details found. Assuming database is prepared and seeded. Skipping Seeder run.")

        self.load_cv_data_to_memory()
        print("BackendManager: Backend initialization complete.")

    def load_cv_data_to_memory(self):
        """
        Loads all relevant CV texts into memory for efficient searching.
        This should happen once on application startup or when new CVs are added.
        """
        application_details = self.db_manager.get_all_application_details()
        cv_paths = [
            detail.cv_path for detail in application_details if detail.cv_path]
        print(f"Loading {len(cv_paths)} CVs into memory...")
        self.in_memory_cv_texts = self.cv_processor.process_cv_for_pattern_matching(
            cv_paths)

    def search_cvs(self, keywords: list[str], algorithm: str, top_n_matches: int = 10, fuzzy_threshold: float = 80) -> dict:
        """
        Performs CV search based on keywords using the specified algorithm via SearchService.
        Returns structured results including exact and fuzzy matches.
        """
        results = []
        total_exact_match_time_ms = 0
        total_fuzzy_match_time_ms = 0

        keywords_lower = [k.lower() for k in keywords]
        exact_matches = {}

        if algorithm.lower() == 'aho-corasick':
            print(
                f"Starting exact matching with Aho-Corasick for keywords: {keywords_lower}")
            for cv_path, text in self.in_memory_cv_texts.items():

                ac_results_for_cv, time_taken = Utils.time_function(
                    self.search_service.search_aho_corasick,
                    text.lower(),
                    keywords_lower
                )
                total_exact_match_time_ms += time_taken
                current_cv_matched_keywords = {}
                current_total_occurrences = 0
                if ac_results_for_cv:
                    for keyword_found, occurrences in ac_results_for_cv.items():
                        if occurrences:
                            current_cv_matched_keywords[keyword_found] = len(
                                occurrences)
                            current_total_occurrences += len(occurrences)

                if current_total_occurrences > 0:
                    exact_matches[cv_path] = {
                        'matched_keywords': current_cv_matched_keywords,
                        'total_occurrences': current_total_occurrences
                    }
        else:
            exact_search_func = None
            algo_name_for_print = ""
            if algorithm.lower() == 'kmp':
                algo_name_for_print = "KMP"
                exact_search_func = self.search_service.search_kmp
            elif algorithm.lower() == 'boyer-moore':
                algo_name_for_print = "Boyer-Moore"
                exact_search_func = self.search_service.search_boyer_moore
            else:
                print(
                    f"Warning: Unknown exact match algorithm '{algorithm}'. Defaulting to KMP.")
                algo_name_for_print = "KMP (defaulted)"
                exact_search_func = self.search_service.search_kmp

            print(
                f"Starting exact matching with {algo_name_for_print} for keywords: {keywords_lower}")

            for cv_path, text in self.in_memory_cv_texts.items():
                current_cv_matched_keywords = {}
                current_total_occurrences = 0
                current_cv_loop_time = 0

                for keyword in keywords_lower:
                    occurrences, time_taken = Utils.time_function(
                        exact_search_func, text.lower(), keyword)
                    current_cv_loop_time += time_taken
                    if occurrences:
                        current_cv_matched_keywords[keyword] = len(occurrences)
                        current_total_occurrences += len(occurrences)

                if current_total_occurrences > 0:
                    exact_matches[cv_path] = {
                        'matched_keywords': current_cv_matched_keywords,
                        'total_occurrences': current_total_occurrences
                    }
                total_exact_match_time_ms += current_cv_loop_time

        sorted_exact_matches = sorted(exact_matches.items(),
                                      key=lambda item: item[1]['total_occurrences'], reverse=True)

        unmatched_keywords = []
        for keyword in keywords:

            keyword_l = keyword.lower()
            found_in_exact = False
            for _, details in sorted_exact_matches:
                if keyword_l in details['matched_keywords']:
                    found_in_exact = True
                    break
            if not found_in_exact:
                unmatched_keywords.append(keyword)

        fuzzy_matches = {}
        print(
            f"Starting fuzzy matching for unmatched keywords: {unmatched_keywords}")

        if unmatched_keywords and fuzzy_threshold is not None:
            for cv_path, text in self.in_memory_cv_texts.items():
                cv_fuzzy_keywords = {}
                highest_cv_similarity = 0.0
                current_cv_loop_fuzzy_time = 0

                cv_words = re.findall(r'\b\w+\b', text.lower())

                for um_keyword in unmatched_keywords:
                    best_similarity_for_keyword = 0.0
                    for cv_word in cv_words:

                        similarity_score, time_taken = Utils.time_function(
                            self.search_service.get_similarity_percentage,
                            um_keyword.lower(), cv_word
                        )
                        current_cv_loop_fuzzy_time += time_taken
                        if similarity_score >= fuzzy_threshold and similarity_score > best_similarity_for_keyword:
                            best_similarity_for_keyword = similarity_score

                    if best_similarity_for_keyword > 0:
                        cv_fuzzy_keywords[um_keyword] = best_similarity_for_keyword
                        if best_similarity_for_keyword > highest_cv_similarity:
                            highest_cv_similarity = best_similarity_for_keyword

                if highest_cv_similarity > 0:
                    fuzzy_matches[cv_path] = {
                        'fuzzy_matched_keywords': cv_fuzzy_keywords,
                        'highest_similarity': highest_cv_similarity
                    }
                total_fuzzy_match_time_ms += current_cv_loop_fuzzy_time

        final_results = []
        processed_cv_paths = set()

        for cv_path, details in sorted_exact_matches:
            application_detail_list = self.db_manager.get_all_application_details()
            app_detail = next(
                (ad for ad in application_detail_list if ad.cv_path == cv_path), None)

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

        sorted_fuzzy_matches = sorted(fuzzy_matches.items(),
                                      key=lambda item: item[1]['highest_similarity'], reverse=True)

        for cv_path, details in sorted_fuzzy_matches:
            if cv_path not in processed_cv_paths:
                application_detail_list = self.db_manager.get_all_application_details()
                app_detail = next(
                    (ad for ad in application_detail_list if ad.cv_path == cv_path), None)
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
            "exact_match_time_ms": total_exact_match_time_ms,
            "fuzzy_match_time_ms": total_fuzzy_match_time_ms if unmatched_keywords else 0
        }

    def get_cv_summary(self, applicant_id: int) -> dict:

        profile = self.db_manager.get_applicant_profile_by_id(applicant_id)
        if not profile:
            return {"error": "Applicant not found."}

        application_details_row = self.db_manager._execute_query(
            "SELECT * FROM ApplicationDetail WHERE applicant_id = %s ORDER BY detail_id DESC LIMIT 1",
            (applicant_id,), fetch_one=True
        )
        if not application_details_row:
            return {"error": "CV details not found for this applicant."}

        cv_path = application_details_row['cv_path']
        if not cv_path or not os.path.exists(cv_path):
            return {"error": f"CV file not found at {cv_path}"}

        cv_text = self.cv_processor.extract_text_from_pdf(cv_path)
        if not cv_text:
            return {"error": "Could not extract text from CV."}

        summary = {
            "applicant_profile": self._get_applicant_profile(applicant_id),
            "extracted_info": {
                "skills": self.regex_extractor.extract_skills(cv_text),
                "job_history": self.regex_extractor.extract_job_history(cv_text),
                "education": self.regex_extractor.extract_education(cv_text)
            }
        }
        return summary

    def get_raw_cv_path(self, applicant_id: int) -> str:
        application_details_row = self.db_manager._execute_query(
            "SELECT cv_path FROM ApplicationDetail WHERE applicant_id = %s ORDER BY detail_id DESC LIMIT 1",
            (applicant_id,), fetch_one=True
        )
        if application_details_row:
            return application_details_row['cv_path']
        return None
    
    def get_full_cv_text(self, applicant_id: int) -> str:
        """
        Retrieves the full CV text for a given applicant ID.
        Returns the text if found, otherwise returns an error message.
        """
        cv_path = self.get_raw_cv_path(applicant_id)
        if not cv_path or not os.path.exists(cv_path):
            return "CV file not found."

        cv_text = self.cv_processor.extract_text_from_pdf(cv_path)
        if not cv_text:
            return "Could not extract text from CV."
        
        return cv_text
    
    def _get_applicant_profile(self, applicant_id: int) -> dict:
        """
        Retrieves the applicant profile and CV summary for a given applicant ID.
        Returns a dictionary with applicant info and extracted CV details.
        first_name, last_name, date_of_birth, address, phone_number
        """
        profile = self.db_manager.get_applicant_profile_by_id(applicant_id)
        if not profile:
            return {"error": "Applicant not found."}

        return {
            "applicant_id": profile.applicant_id,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "date_of_birth": profile.date_of_birth,
            "address": profile.address,
            "phone_number": profile.phone_number
        }
    
    def shutdown_backend(self):
        """Closes any open connections."""
        self.db_manager.close()
