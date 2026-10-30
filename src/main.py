import csv
from pathlib import Path
from validator import validate_invoices
from database import insert_invoices
from excel_export import export_invoices
from reports import generate_reports
from report_export import export_reports

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "input" / "Invoices.csv"

with open(file_path, mode="r", newline="") as file:
    reader = csv.DictReader(file)
    invoices = list(reader)

valid, invalid, duplicates = validate_invoices(invoices)

print("\nINVOICE PROCESSING SUMMARY")
print("--------------------------")
print("Total invoices:", len(invoices))
print("Valid invoices:", len(valid))
print("Invalid invoices:", len(invalid))
print("Duplicate invoices:", len(duplicates))

inserted = insert_invoices(valid)

print("\nDATABASE SUMMARY")
print("----------------")
print("Invoices inserted into MySQL:", inserted)
export_invoices()
generate_reports()
export_reports()