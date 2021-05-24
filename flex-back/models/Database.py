import psycopg2

class Database:
    def __init__(self, dbName, user, password):
        connection = psycopg2.connect("dbname=" + dbName + " user=" + user + " password=" + password)
        cursor = conn.cursor()

    def initializeDB(self):
        commands = (
            """
            
            """
        )