import os
from backend.models import ApplicantProfile, ApplicationDetail
from backend.database_manager import DatabaseManager


class Seeder:
    """
    Handles scanning the data directory for CV files and seeding
    the ApplicationDetail table. It uses a single common ApplicantProfile
    for all entries and infers application_role from the directory structure.
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.common_applicant_id = None

    def _ensure_common_applicant_profile(self):
        """
        Ensures that a common applicant profile exists for this seeding session
        and its ID is available in self.common_applicant_id.
        If not already set in this session, it creates a new "Default Applicant".
        Note: For true idempotency across multiple script runs (not just sessions),
        a check for an existing "Default Applicant" by name in the DB would be needed
        (e.g., using a db_manager.get_applicant_profile_by_name method).
        """
        if self.common_applicant_id is None:

            common_profile = ApplicantProfile(
                first_name="Default",
                last_name="Applicant"
            )

            applicant_id = self.db_manager.insert_applicant_profile(
                common_profile)

            if applicant_id:
                self.common_applicant_id = applicant_id
                print(
                    f"Established common applicant profile: ID {self.common_applicant_id} (Name: Default Applicant)")
            else:
                error_msg = "Error: Could not create common applicant profile."
                print(error_msg)
                raise Exception(error_msg)
        return self.common_applicant_id

    def seed_application_details_from_paths(self, data_directory: str):
        """
        Scans the specified data_directory for PDF CV files,
        and inserts their paths into the ApplicationDetail table.
        Uses a common applicant_id and infers application_role from folder names.

        Args:
            data_directory (str): The root directory containing category folders (e.g., '../data/').
        """
        print(
            f"Starting seeding of ApplicationDetail table from paths in '{data_directory}'...")

        try:
            self._ensure_common_applicant_profile()
            if not self.common_applicant_id:
                print(
                    "Aborting seeding: Common applicant profile ID could not be established.")
                return
        except Exception as e:
            print(f"Error during common profile setup: {e}. Aborting seeding.")
            return

        processed_cv_paths = set()

        existing_details = self.db_manager.get_all_application_details()
        for detail in existing_details:
            if detail.cv_path:
                processed_cv_paths.add(os.path.normpath(detail.cv_path))

        for root, dirs, files in os.walk(data_directory):
            norm_root = os.path.normpath(root)
            norm_data_directory = os.path.normpath(data_directory)

            application_role_candidate = os.path.basename(norm_root)

            if norm_root == norm_data_directory:
                print(
                    f"Scanning root data directory: {norm_root}. Subdirectories will be processed for roles.")
                continue

            if not application_role_candidate:
                print(
                    f"  Skipping directory with empty role name in '{norm_root}'")
                continue

            print(
                f"Processing role: '{application_role_candidate}' from directory: '{norm_root}'")

            for file_name in files:
                if file_name.lower().endswith('.pdf'):

                    cv_path_full = os.path.abspath(
                        os.path.join(norm_root, file_name))

                    cv_path_norm = os.path.normpath(cv_path_full)

                    if cv_path_norm in processed_cv_paths:
                        print(
                            f"  Skipping '{file_name}': Already seeded (Path: {cv_path_norm}).")
                        continue

                    if not os.path.exists(cv_path_full):
                        print(
                            f"  Warning: File '{file_name}' listed by os.walk but not found at '{cv_path_full}'. Skipping.")
                        continue

                    print(
                        f"  Attempting to seed ApplicationDetail for: {file_name}")

                    app_detail = ApplicationDetail(
                        applicant_id=self.common_applicant_id,
                        application_role=application_role_candidate,
                        cv_path=cv_path_full
                    )

                    inserted_detail_id = self.db_manager.insert_application_detail(
                        app_detail)

                    if inserted_detail_id:
                        print(
                            f"    Successfully seeded ApplicationDetail for '{file_name}' (Role: {application_role_candidate}, ApplicantID: {self.common_applicant_id}, DetailID: {inserted_detail_id})")
                        processed_cv_paths.add(cv_path_norm)
                    else:
                        print(
                            f"    Failed to insert ApplicationDetail for '{file_name}'.")

        print("ApplicationDetail seeding from paths complete.")
