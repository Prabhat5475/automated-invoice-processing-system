
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

load_dotenv(os.path.join(project_folder, ".env"))


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        return connection

    except Error as error:
        print("MySQL connection failed:", error)
        return None
