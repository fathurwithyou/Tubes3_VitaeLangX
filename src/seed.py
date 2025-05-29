from backend import *

if __name__ == '__main__':

    db_manager = DatabaseManager(
        host='localhost', user='root', password='', db='ats_db')
    db_manager.connect()

    db_manager.create_tables()

    data_dir = '../data/'

    seeder = Seeder(db_manager)
    seeder.seed_application_details_from_paths(data_dir)

    db_manager.close()
