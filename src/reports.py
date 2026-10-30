from db_connection import create_connection


def generate_reports():
    connection = create_connection()
    if connection is None:
        print("Cannot generate reports: Database connection failed.")
        return
    cursor = connection.cursor()

    print("\n========== INVOICE REPORTS ==========")

    # 1. Total invoices and revenue
    cursor.execute("""
        SELECT COUNT(*), SUM(amount)
        FROM invoices
    """)

    total, revenue = cursor.fetchone()

    print("\nTotal invoices:", total)
    print("Total revenue:", revenue)

    # 2. Paid and pending invoices
    cursor.execute("""
        SELECT status, COUNT(*), SUM(amount)
        FROM invoices
        GROUP BY status
    """)

    print("\nPAYMENT SUMMARY")

    for status, count, amount in cursor.fetchall():
        print(status, "| Count:", count, "| Amount:", amount)

    # 3. Customer-wise revenue
    cursor.execute("""
        SELECT customer_name, COUNT(*), SUM(amount)
        FROM invoices
        GROUP BY customer_name
        ORDER BY SUM(amount) DESC
    """)

    print("\nCUSTOMER-WISE REPORT")

    for customer, count, amount in cursor.fetchall():
        print(customer, "| Invoices:", count, "| Revenue:", amount)

    cursor.close()
    connection.close()