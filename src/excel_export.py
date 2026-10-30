from pathlib import Path
from openpyxl import Workbook
from db_connection import create_connection


def export_invoices():
    connection = create_connection()
    if connection is None:
        print("Cannot export invoices: Database connection failed.")
        return
    cursor = connection.cursor()

    cursor.execute("""
        SELECT invoice_id, customer_name, invoice_date, amount, status
        FROM invoices
        ORDER BY invoice_date
    """)

    records = cursor.fetchall()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Processed Invoices"

    # Add column headings
    sheet.append([
        "Invoice ID",
        "Customer Name",
        "Invoice Date",
        "Amount",
        "Status"
    ])

    # Make headings bold
    from openpyxl.styles import Font

    for cell in sheet[1]:
        cell.font = Font(bold=True)

    # Adjust column widths
    sheet.column_dimensions["A"].width = 18
    sheet.column_dimensions["B"].width = 25
    sheet.column_dimensions["C"].width = 18
    sheet.column_dimensions["D"].width = 15
    sheet.column_dimensions["E"].width = 15

    # Add invoice records
    for record in records:
        sheet.append(list(record))

    # Save Excel file
    project_folder = Path(__file__).resolve().parent.parent
    output_folder = project_folder / "data" / "output"
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "Processed_Invoices.xlsx"
    workbook.save(output_file)

    cursor.close()
    connection.close()

    print("\nExcel file generated successfully!")
    print("File location:", output_file)