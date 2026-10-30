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
- **Automated Testing:** Includes unit tests for invoice validation.

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
│   └── test_validator.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/Prabhat5475/automated-invoice-processing-system.git
cd automated-invoice-processing-system
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Install and start MySQL Server.

5. Create a database named `invoice_processor` and an `invoices` table using the schema below.

6. Create a MySQL user with the required database permissions.

7. Create a `.env` file in the project root using `.env.example` as a reference. Add your own MySQL credentials.

8. Place the input CSV file inside `data/input/`.

## Database Schema

```sql
CREATE DATABASE invoice_processor;

USE invoice_processor;

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

## Run Automated Tests

```bash
python -m unittest discover -s tests -v
```

## Generated Reports

The system generates two Excel workbooks inside `data/output/`:

1. `Processed_Invoices.xlsx` – Contains processed invoice records.
2. `Invoice_Reports.xlsx` – Contains overall summary, payment summary, and customer-wise revenue reports.

## Current Test Results

Using the current sample dataset:

- Total input records: 13
- Valid invoices: 11
- Invalid invoices: 1
- Duplicate invoices: 1
- Stored invoices: 11
- Total invoice revenue: ₹2,20,500

The validation module currently has 10 automated tests.

## Future Improvements

- Automated email notifications.
- PDF invoice processing.
- Improved logging and exception handling.
- A graphical user interface.

## Project Inspiration

The workflow was inspired by an Excel/VBA-based invoice management project. This implementation independently uses Python and MySQL for invoice validation, storage, and reporting.