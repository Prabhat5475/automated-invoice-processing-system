# Automated Invoice Processing System

A Python-based invoice processing system that reads invoice records from CSV files, validates data, detects duplicate invoices, stores valid records in MySQL, and generates Excel reports.

## Features

- **CSV Input:** Reads invoice records from CSV files.
- **Data Validation:** Checks required fields, invoice dates, amounts, and payment statuses.
- **Duplicate Detection:** Identifies duplicate invoice IDs.
- **MySQL Integration:** Stores valid invoices in a MySQL database.
- **Duplicate-safe Insertion:** Prevents existing invoice IDs from being inserted again.
- **Excel Export:** Generates formatted Excel files containing processed invoices.
- **Financial Reports:** Generates revenue, payment status, and customer-wise reports.
- **Report Export:** Exports financial reports into a separate Excel workbook.

## Technology Stack

- Python
- MySQL
- SQL
- CSV
- OpenPyXL
- Python-dotenv
- Git and GitHub

## Project Structure

```text
Invoice_process/
│
├── data/
│   ├── input/
│   │   └── Invoices.csv
│   └── output/
│
├── src/
│   ├── main.py
│   ├── validator.py
│   ├── db_connection.py
│   ├── database.py
│   ├── excel_export.py
│   ├── reports.py
│   └── report_export.py
│
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Create a MySQL database named `invoice_processor`.
5. Create the `invoices` table using the SQL schema provided below.
6. Configure your database credentials in a `.env` file.
7. Place the input CSV file inside `data/input/`.

## Database Schema

```sql
CREATE TABLE invoices (
    invoice_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    invoice_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL
);
```

## Run the Project

```bash
python src/main.py
```

## Generated Reports

The system generates two Excel workbooks:

1. `Processed_Invoices.xlsx` – Contains processed invoice records.
2. `Invoice_Reports.xlsx` – Contains overall summary, payment summary, and customer-wise revenue reports.

Both files are generated inside `data/output/`.

## Current Test Results

Using the sample dataset:

- Total input records: 12
- Valid invoices: 10
- Invalid invoices: 1
- Duplicate invoices: 1
- Stored invoices: 10
- Total invoice revenue: ₹1,80,500

## Future Improvements

- Automated email notifications.
- PDF invoice processing.
- Unit testing.
- Improved logging and exception handling.
- A graphical user interface.

## Project Inspiration

The workflow was inspired by an Excel/VBA-based invoice management project. This implementation independently uses Python and MySQL for invoice validation, storage, and reporting.