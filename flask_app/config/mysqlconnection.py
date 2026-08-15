import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv() # lee el archivo .env cuando trabajas en local
class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host=os.environ.get('DB_HOST'),
            port=int(os.environ.get('DB_PORT', 3306)),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
            )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                query_limpia = query.lower().strip()
                if query_limpia.startswith("insert"):
                    self.connection.commit()
                    return cursor.lastrowid
                elif query_limpia.startswith("select"):
                    return cursor.fetchall()
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
