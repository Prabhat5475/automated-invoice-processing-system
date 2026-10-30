
import mysql.connector
from mysql.connector import Error
from db_connection import create_connection


def insert_invoices(invoices):
    connection = None
    cursor = None
    inserted_count = 0
    failed_count = 0

    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = """
            INSERT IGNORE INTO invoices
            (invoice_id, customer_name, invoice_date, amount, status)
            VALUES (%s, %s, %s, %s, %s)
        """

        for invoice in invoices:
            values = (
                invoice["invoice_id"],
                invoice["customer_name"],
                invoice["invoice_date"],
                float(invoice["amount"]),
                invoice["status"].upper()
            )

            try:
                cursor.execute(query, values)

                if cursor.rowcount == 1:
                    inserted_count += 1

            except (Error, ValueError) as error:
                failed_count += 1
                print("Failed:", invoice["invoice_id"], error)

        connection.commit()

        print("Failed insertions:", failed_count)

    except Error as error:
        print("Database error:", error)
        if connection:
            connection.rollback()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

    return inserted_count
