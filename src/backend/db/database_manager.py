import pymysql.cursors
from backend.models import ApplicantProfile, ApplicationDetail
from backend.encryption import VigenereCipher
import datetime
import os


class DatabaseManager:
    """
    Manages connections and operations for the MySQL database.
    """

    def __init__(self, host='localhost', user='root', password='', db='ats_db'):
        self.connection = None
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.encryptor = VigenereCipher(key="i-see-the-key")

    def connect(self):
        """
        Establishes a connection to the database.
        If the database does not exist, it attempts to create it.
        """
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"Database '{self.db}' connected successfully.")
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1049:
                print(
                    f"Database '{self.db}' not found. Attempting to create it...")
                try:
                    conn_server = pymysql.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        cursorclass=pymysql.cursors.DictCursor
                    )
                    with conn_server.cursor() as cursor:

                        cursor.execute(
                            f"CREATE DATABASE IF NOT EXISTS `{self.db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    conn_server.commit()
                    conn_server.close()
                    print(f"Database '{self.db}' created successfully.")

                    self.connection = pymysql.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.db,
                        cursorclass=pymysql.cursors.DictCursor
                    )
                    print(
                        f"Database '{self.db}' connected successfully after creation.")
                except pymysql.Error as ce:
                    print(f"Error creating database '{self.db}': {ce}")
                    self.connection = None
                except Exception as ex_creation:
                    print(
                        f"An unexpected error occurred during database creation: {ex_creation}")
                    self.connection = None
            else:
                print(
                    f"Error connecting to database '{self.db}' (OperationalError other than Unknown DB): {e}")
                self.connection = None
        except pymysql.Error as e_pymysql:
            print(
                f"A PyMySQL error occurred during connection attempt: {e_pymysql}")
            self.connection = None
        except Exception as ex_general:
            print(
                f"An unexpected error occurred during connection: {ex_general}")
            self.connection = None

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def _execute_query(self, query: str, params: tuple = None, fetch_one=False, fetch_all=False, commit=False):
        """Internal method to execute SQL queries."""
        if not self.connection:
            self.connect()
            if not self.connection:
                return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if commit:
                    self.connection.commit()
                if fetch_one:
                    return cursor.fetchone()
                if fetch_all:
                    return cursor.fetchall()
                return cursor.lastrowid
        except pymysql.Error as e:
            print(f"Database query error: {e}")
            if commit:
                try:
                    self.connection.rollback()
                except pymysql.Error as rb_err:
                    print(f"Error during rollback: {rb_err}")
            return None
        except Exception as ex:
            print(f"An unexpected error occurred during query execution: {ex}")
            return None

    def create_tables(self):
        """Creates the necessary tables if they don't exist."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS ApplicantProfile (
                applicant_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) DEFAULT NULL,
                last_name VARCHAR(50) DEFAULT NULL,
                date_of_birth DATE DEFAULT NULL,
                address VARCHAR(255) DEFAULT NULL,
                phone_number VARCHAR(20) DEFAULT NULL 
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ApplicationDetail (
                detail_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                applicant_id INT NOT NULL,
                application_role VARCHAR(100) DEFAULT NULL,
                cv_path TEXT,
                FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id)
            )
            """
        ]
        for query in queries:
            self._execute_query(query, commit=True)
        print("Tables checked/created.")

    def insert_applicant_profile(self, profile: ApplicantProfile) -> int:
        """Inserts a new applicant profile into the database."""
        query = """
        INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
        VALUES (%s, %s, %s, %s, %s)
        """
        profile.first_name = self.encryptor.encrypt(profile.first_name)
        profile.last_name = self.encryptor.encrypt(profile.last_name)
        profile.address = self.encryptor.encrypt(profile.address)
        profile.phone_number = self.encryptor.encrypt(profile.phone_number)
        params = (profile.first_name, profile.last_name, profile.date_of_birth,
                  profile.address, profile.phone_number)

        return self._execute_query(query, params, commit=True)

    def insert_application_detail(self, detail: ApplicationDetail) -> int:
        """Inserts new application details into the database."""
        query = """
        INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
        VALUES (%s, %s, %s)
        """
        params = (detail.applicant_id, detail.application_role, detail.cv_path)
        return self._execute_query(query, params, commit=True)

    def get_all_application_details(self) -> list[ApplicationDetail]:
        """Retrieves all application details."""
        query = "SELECT * FROM ApplicationDetail"
        rows = self._execute_query(query, fetch_all=True)
        if rows:
            return [ApplicationDetail(**row) for row in rows]
        return []

    def get_applicant_profile_by_id(self, applicant_id: int) -> ApplicantProfile:
        """Retrieves an applicant profile by their ID."""
        query = "SELECT * FROM ApplicantProfile WHERE applicant_id = %s"
        params = (applicant_id,)
        row = self._execute_query(query, params, fetch_one=True)
        if row:
            return ApplicantProfile(**row)
        return None

    def get_total_cv_count(self) -> int:
        """Returns the total number of CVs in the database."""
        query = "SELECT COUNT(*) AS total FROM ApplicationDetail"
        row = self._execute_query(query, fetch_one=True)
        if row:
            return row['total']
        return 0
