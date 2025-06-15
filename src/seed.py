from backend import DatabaseManager, Seeder
from backend.encryption import VigenereCipher

if __name__ == "__main__":
    db_manager = DatabaseManager(
        host="localhost", user="root", password="", db="ats_db"
    )

    try:
        db_manager.connect()
        print("Connected to database")

        db_manager.create_tables()
        print("Tables created/verified")

        seeder = Seeder(db_manager, VigenereCipher("i-see-the-key"))

        sql_file = "../seeds/tubes3_seeding.sql"
        seeder.seed_and_encrypt(sql_file)

        print("Seeding and encryption process completed successfully")

    except Exception as e:
        print(f"Error: {e}")
