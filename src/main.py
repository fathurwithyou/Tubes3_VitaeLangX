import os
from backend.core_manager import BackendManager


def main():
    print("Initializing ATS Backend...")

    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)
    # os.makedirs(os.path.join(data_dir, 'HR'), exist_ok=True)
    # os.makedirs(os.path.join(data_dir, 'Sales'), exist_ok=True)

    backend_manager = BackendManager()
    backend_manager.initialize_backend(data_directory=data_dir)

    print("\nBackend initialized. You can now integrate with a frontend.")
    print("Example usage (simulated from frontend interaction):")

    keywords_kmp = ["python", "react", "sql"]
    print(f"\n--- Searching for {keywords_kmp} using KMP (Top 5 Matches) ---")
    search_results_kmp = backend_manager.search_cvs(
        keywords_kmp, "KMP", top_n_matches=5, fuzzy_threshold=80)
    print(
        f"Exact Match Search Time: {search_results_kmp['exact_match_time_ms']:.2f} ms")
    print(
        f"Fuzzy Match Search Time: {search_results_kmp['fuzzy_match_time_ms']:.2f} ms")
    for i, result in enumerate(search_results_kmp['results']):
        print(
            f"Match {i+1}: {result['name']} (CV: {os.path.basename(result['cv_path'])})")
        if result['matched_keywords']:
            print(
                f"  Exact Keywords ({result['total_occurrences']} total occurrences): {result['matched_keywords']}")
        if result['fuzzy_keywords']:
            print(
                f"  Fuzzy Keywords (Highest Similarity: {result['highest_fuzzy_similarity']:.2f}%): {result['fuzzy_keywords']}")

    keywords_bm = ["java", "spring boot", "database"]
    print(f"\n--- Searching for {keywords_bm} using BM (Top 3 Matches) ---")
    search_results_bm = backend_manager.search_cvs(
        keywords_bm, "BM", top_n_matches=3, fuzzy_threshold=80)
    print(
        f"Exact Match Search Time: {search_results_bm['exact_match_time_ms']:.2f} ms")
    print(
        f"Fuzzy Match Search Time: {search_results_bm['fuzzy_match_time_ms']:.2f} ms")
    for i, result in enumerate(search_results_bm['results']):
        print(
            f"Match {i+1}: {result['name']} (CV: {os.path.basename(result['cv_path'])})")
        if result['matched_keywords']:
            print(
                f"  Exact Keywords ({result['total_occurrences']} total occurrences): {result['matched_keywords']}")
        if result['fuzzy_keywords']:
            print(
                f"  Fuzzy Keywords (Highest Similarity: {result['highest_fuzzy_similarity']:.2f}%): {result['fuzzy_keywords']}")

    summary = backend_manager.get_cv_summary(4)
    if "error" not in summary:
        print(f"Name: {summary['applicant_info']['name']}")
        print(f"Birthdate: {summary['applicant_info']['birthdate']}")
        print(f"Address: {summary['applicant_info']['address']}")
        print(f"Phone: {summary['applicant_info']['phone_number']}")
        print(f"\nSummary: {summary['extracted_info']['summary_text']}")
        print(f"Skills: {', '.join(summary['extracted_info']['skills'])}")
        print("Job History:")
        for job in summary['extracted_info']['job_history']:
            print(f"  - {job['title']} at {job['company']} ({job['dates']})")
            print(f"    Description: {job['description']}")
        print("Education:")
        for edu in summary['extracted_info']['education']:
            print(
                f"  - {edu['degree']} from {edu['university']} ({edu['dates']})")
    else:
        print(f"Error getting summary: {summary['error']}")

    print(f"\n--- Getting Raw CV Path for Applicant ID 4 ---")
    raw_cv_path = backend_manager.get_raw_cv_path(4)
    print(f"Raw CV Path: {raw_cv_path}")

    backend_manager.shutdown_backend()
    print("\nBackend shut down.")

if __name__ == "__main__":
    main()
