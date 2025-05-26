import datetime

class ApplicantProfile:
    """
    Represents an applicant's personal profile information.
    Corresponds to the ApplicantProfile table in the database.
    """
    def __init__(self, applicant_id: int = None, first_name: str = None,
                 last_name: str = None, date_of_birth: datetime.date = None,
                 address: str = None, phone_number: str = None):
        self.applicant_id = applicant_id  # PK
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone_number = phone_number

    def __repr__(self):
        return f"ApplicantProfile(ID: {self.applicant_id}, Name: {self.first_name} {self.last_name})"

class ApplicationDetail:
    """
    Represents the details of an application submitted by an applicant.
    Corresponds to the ApplicationDetail table in the database.
    """
    def __init__(self, detail_id: int = None, applicant_id: int = None,
                 application_role: str = None, cv_path: str = None):
        self.detail_id = detail_id  # PK
        self.applicant_id = applicant_id  # FK to ApplicantProfile
        self.application_role = application_role
        self.cv_path = cv_path

    def __repr__(self):
        return f"ApplicationDetail(ID: {self.detail_id}, ApplicantID: {self.applicant_id}, Role: {self.application_role})"