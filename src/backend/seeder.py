import os
import logging
from backend.db.database_manager import DatabaseManager
from backend.encryption import VigenereCipher


class Seeder:
    """
    Seeder class to populate the database with initial data.
    """

    def __init__(
        self, db_manager: DatabaseManager, encryption_key: str = "i-see-the-key"
    ):
        self.db_manager = db_manager
        self.common_applicant_id = None
        self.encryption = VigenereCipher(encryption_key)
        self.logger = logging.getLogger(__name__)

    def seed_database(self, sql_file: str):
        """
        Seeds the database with the SQL file, then encrypts sensitive data.

        Args:
            sql_file (str): Path to the SQL file containing seed data
        """
        try:
            print("Step 1: Inserting original data...")
            self._execute_sql_file(sql_file)

            print("Step 2: Retrieving data for encryption...")
            self._encrypt_existing_data()

            print("Database seeded and encrypted successfully!")

        except Exception as e:
            self.logger.error(f"Error in seed_database: {e}")
            print(f"Error: {e}")
            if self.db_manager.connection:
                self.db_manager.connection.rollback()

    def _execute_sql_file(self, sql_file: str):
        """
        Execute SQL file normally without encryption using DatabaseManager's method.
        """
        if not os.path.exists(sql_file):
            raise FileNotFoundError(f"SQL file not found: {sql_file}")

        with open(sql_file, "r", encoding="utf-8") as file:
            sql_content = file.read()

        sql_statements = [
            stmt.strip() for stmt in sql_content.split(";") if stmt.strip()
        ]

        for statement in sql_statements:
            try:
                self.db_manager._execute_query(statement, commit=True)
            except Exception as e:
                self.logger.error(f"Error executing SQL: {str(e)}")
                print(f"Error executing statement: {str(e)}")
                continue

        print(f"Executed {len(sql_statements)} SQL statements")

    def _encrypt_existing_data(self):
        """
        Take all data from ApplicantProfile table, encrypt sensitive fields, then update back.
        """
        try:
            print("Encrypting ApplicantProfile data...")

            query = "SELECT * FROM ApplicantProfile"
            records = self.db_manager._execute_query(query, fetch_all=True)

            if not records:
                print("No records found in ApplicantProfile table")
                return

            print(
                f"Found {len(records)} records to encrypt in ApplicantProfile")
            print(
                f"Sample record structure: {list(records[0].keys()) if records else 'No records'}"
            )

            for i, record_dict in enumerate(records, 1):
                try:
                    print(
                        f"Processing record {i}/{len(records)} - applicant_id: {record_dict.get('applicant_id')}"
                    )

                    encrypted_data = {}
                    for column, value in record_dict.items():
                        if self._is_sensitive_field(column) and value:
                            print(f"  Encrypting {column}: '{value}'")
                            encrypted_value = self.encryption.encrypt(
                                str(value))
                            encrypted_data[column] = encrypted_value
                            print(
                                f"  Encrypted {column} for applicant_id {record_dict.get('applicant_id')}"
                            )
                        else:
                            encrypted_data[column] = value

                    self._update_record_dict(
                        "ApplicantProfile", encrypted_data, record_dict["applicant_id"]
                    )

                except Exception as record_error:
                    print(f"Error processing record {i}: {str(record_error)}")
                    self.logger.error(
                        f"Error processing record {i}: {str(record_error)}"
                    )
                    continue

            self.db_manager.connection.commit()
            print("ApplicantProfile encryption completed successfully")
            print("Note: ApplicationDetail table is left unencrypted as requested")

        except Exception as e:
            print(f"Error encrypting data: {str(e)}")
            self.logger.error(f"Error encrypting data: {str(e)}")
            if self.db_manager.connection:
                self.db_manager.connection.rollback()
            raise

    def _is_sensitive_field(self, column_name: str) -> bool:
        """
        Check if a column contains sensitive data that should be encrypted.
        For ApplicantProfile: encrypt all fields except applicant_id and date_of_birth
        """

        sensitive_fields = ["first_name",
                            "last_name", "address", "phone_number"]
        return column_name.lower() in sensitive_fields

    def _update_record_dict(self, table_name: str, data: dict, record_id):
        """
        Update a specific record with encrypted data using DatabaseManager's method.
        """
        try:
            set_clauses = []
            values = []

            id_column = "applicant_id"

            for column, value in data.items():
                if column != id_column:
                    set_clauses.append(f"{column} = %s")
                    values.append(value)

            if not set_clauses:
                print(f"No fields to update for record {record_id}")
                return

            values.append(record_id)

            update_query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE {id_column} = %s"
            print(f"  Executing update for {id_column} = {record_id}")

            result = self.db_manager._execute_query(
                update_query, tuple(values), commit=True
            )

            if result is not None:
                print(f"  Successfully updated record {record_id}")
            else:
                print(f"  Failed to update record {record_id}")

        except Exception as e:
            print(f"Error updating record {record_id}: {str(e)}")
            self.logger.error(f"Error updating record {record_id}: {str(e)}")
            raise

    def encrypt_database(self, key: str):
        """
        Encrypts the database using the provided key.
        Updates the encryption key and re-encrypts all data.
        """
        try:
            print("Updating encryption key and re-encrypting data...")

            self.encryption = VigenereCipher(key)

            self._encrypt_existing_data()

            print("Database re-encrypted with new key")

        except Exception as e:
            self.logger.error(f"Error encrypting database: {e}")
            print(f"Error encrypting database: {e}")

    def decrypt_and_view_data(self, table_name: str = "ApplicantProfile"):
        """
        Decrypt and display data for verification.
        """
        try:
            query = f"SELECT * FROM {table_name} LIMIT 5"
            records = self.db_manager._execute_query(query, fetch_all=True)

            if not records:
                print(f"No records found in {table_name} table")
                return

            for record_dict in records:
                id_column = (
                    "applicant_id" if table_name == "ApplicantProfile" else "detail_id"
                )
                print(f"\nRecord {id_column}: {record_dict.get(id_column)}")

                for column, value in record_dict.items():
                    if self._is_sensitive_field(column) and value:
                        try:
                            decrypted_value = self.encryption.decrypt(
                                str(value))
                            print(
                                f"  {column}: '{decrypted_value}' (decrypted)")
                        except Exception as decrypt_error:
                            print(
                                f"  {column}: '{value}' (failed to decrypt: {decrypt_error})"
                            )
                    else:
                        print(f"  {column}: {value}")

        except Exception as e:
            print(f"Error viewing data: {str(e)}")
            self.logger.error(f"Error viewing data: {str(e)}")
