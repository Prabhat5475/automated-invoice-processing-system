from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font
from db_connection import create_connection


def export_reports():
    connection = create_connection()
    if connection is None:
        print("Cannot export reports: Database connection failed.")
        return
    cursor = connection.cursor()

    workbook = Workbook()

    # Sheet 1: Overall Summary
    summary_sheet = workbook.active
    summary_sheet.title = "Overall Summary"

    cursor.execute("""
        SELECT COUNT(*), SUM(amount)
        FROM invoices
    """)

    total, revenue = cursor.fetchone()

    summary_sheet.append(["Metric", "Value"])
    summary_sheet.append(["Total Invoices", total])
    summary_sheet.append(["Total Revenue", float(revenue or 0)])

    # Sheet 2: Payment Summary
    payment_sheet = workbook.create_sheet("Payment Summary")

    cursor.execute("""
        SELECT status, COUNT(*), SUM(amount)
        FROM invoices
        GROUP BY status
    """)

    payment_sheet.append(["Status", "Invoice Count", "Total Amount"])

    for status, count, amount in cursor.fetchall():
        payment_sheet.append([status, count, float(amount)])

    # Sheet 3: Customer Report
    customer_sheet = workbook.create_sheet("Customer Report")

    cursor.execute("""
        SELECT customer_name, COUNT(*), SUM(amount)
        FROM invoices
        GROUP BY customer_name
        ORDER BY SUM(amount) DESC
    """)

    customer_sheet.append([
        "Customer Name",
        "Invoice Count",
        "Total Revenue"
    ])

    for customer, count, amount in cursor.fetchall():
        customer_sheet.append([customer, count, float(amount)])

    # Format headings and columns
    for sheet in workbook.worksheets:
        for cell in sheet[1]:
            cell.font = Font(bold=True)

        for column in sheet.columns:
            column_letter = column[0].column_letter
            max_length = max(len(str(cell.value or "")) for cell in column)
            sheet.column_dimensions[column_letter].width = max_length + 4

    # Save workbook
    project_folder = Path(__file__).resolve().parent.parent
    output_folder = project_folder / "data" / "output"
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "Invoice_Reports.xlsx"
    workbook.save(output_file)

    cursor.close()
    connection.close()

    print("\nFinancial reports exported successfully!")
    print("File location:", output_file)