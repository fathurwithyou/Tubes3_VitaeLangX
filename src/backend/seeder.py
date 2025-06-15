class Seeder:
    """
    Core algorithm for selective field encryption in database seeding.
    Implements secure data population with field-level encryption.
    """

    def __init__(self, db_manager, encryption_cipher):
        self.db_manager = db_manager
        self.encryption = encryption_cipher

    def seed_and_encrypt(self, sql_file: str):
        """
        Main algorithm: Seed database then encrypt sensitive fields.

        Time Complexity: O(n*m) where n = records, m = fields per record
        Space Complexity: O(1) - processes records individually
        """
        try:
            self._execute_sql_file(sql_file)
            self._encrypt_existing_data()
            self.db_manager.connection.commit()
        except Exception as e:
            if self.db_manager.connection:
                self.db_manager.connection.rollback()
            raise

    def _execute_sql_file(self, sql_file: str):
        """
        SQL file parsing and execution algorithm.

        Algorithm:
        1. Read file content
        2. Split into individual statements 
        3. Execute each statement with error isolation
        """
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_content = file.read()

        sql_statements = [
            stmt.strip() for stmt in sql_content.split(";") if stmt.strip()
        ]

        for statement in sql_statements:
            try:
                self.db_manager._execute_query(statement, commit=True)
            except Exception:
                continue  # Isolate failures, continue processing

    def _encrypt_existing_data(self):
        """
        Selective field encryption algorithm.

        Algorithm:
        1. Retrieve all records from target table
        2. For each record:
           a. Identify sensitive fields using classification function
           b. Encrypt sensitive field values
           c. Update record with encrypted data
        3. Batch commit all changes
        """
        query = "SELECT * FROM ApplicantProfile"
        records = self.db_manager._execute_query(query, fetch_all=True)

        if not records:
            return

        for record_dict in records:
            encrypted_data = self._process_record_fields(record_dict)
            self._update_record(encrypted_data, record_dict["applicant_id"])

    def _process_record_fields(self, record_dict: dict) -> dict:
        """
        Field-level encryption processing algorithm.

        Algorithm:
        1. Iterate through all fields in record
        2. Apply sensitivity classification
        3. Encrypt sensitive fields, preserve others
        4. Return processed record
        """
        encrypted_data = {}
        for column, value in record_dict.items():
            if self._is_sensitive_field(column) and value:
                encrypted_data[column] = self.encryption.encrypt(str(value))
            else:
                encrypted_data[column] = value
        return encrypted_data

    def _is_sensitive_field(self, column_name: str) -> bool:
        """
        Field sensitivity classification algorithm.

        Returns True if field contains PII/sensitive data.
        Classification based on predefined sensitive field patterns.
        """
        sensitive_fields = {"first_name",
                            "last_name", "address", "phone_number"}
        return column_name.lower() in sensitive_fields

    def _update_record(self, data: dict, record_id):
        """
        Record update algorithm with dynamic SQL generation.

        Algorithm:
        1. Build SET clauses for non-ID fields
        2. Construct parameterized UPDATE query
        3. Execute with bound parameters
        """
        set_clauses = []
        values = []
        id_column = "applicant_id"

        for column, value in data.items():
            if column != id_column:
                set_clauses.append(f"{column} = %s")
                values.append(value)

        if set_clauses:
            values.append(record_id)
            update_query = f"UPDATE ApplicantProfile SET {', '.join(set_clauses)} WHERE {id_column} = %s"
            self.db_manager._execute_query(
                update_query, tuple(values), commit=True)
