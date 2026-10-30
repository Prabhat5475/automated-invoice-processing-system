
import sys
import unittest
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_folder / "src"))

from validator import validate_invoices


class TestInvoiceValidator(unittest.TestCase):

    def setUp(self):
        self.invoice = {
            "invoice_id": "INV100",
            "customer_name": "Test Company",
            "invoice_date": "2026-10-15",
            "amount": "15000",
            "status": "PAID"
        }

    def test_valid_invoice(self):
        valid, invalid, duplicates = validate_invoices(
            [self.invoice.copy()]
        )

        self.assertEqual(len(valid), 1)
        self.assertEqual(len(invalid), 0)
        self.assertEqual(len(duplicates), 0)

    def test_invalid_amount(self):
        invoice = self.invoice.copy()
        invoice["amount"] = "-500"

        valid, invalid, duplicates = validate_invoices([invoice])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_duplicate_invoice(self):
        invoice1 = self.invoice.copy()
        invoice2 = self.invoice.copy()

        valid, invalid, duplicates = validate_invoices(
            [invoice1, invoice2]
        )

        self.assertEqual(len(valid), 1)
        self.assertEqual(len(duplicates), 1)

    def test_invalid_date(self):
        invoice = self.invoice.copy()
        invoice["invoice_date"] = "wrong-date"

        valid, invalid, duplicates = validate_invoices([invoice])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_invalid_status(self):
        invoice = self.invoice.copy()
        invoice["status"] = "UNKNOWN"

        valid, invalid, duplicates = validate_invoices([invoice])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_missing_customer_name(self):
        invoice = self.invoice.copy()
        invoice["customer_name"] = ""

        valid, invalid, duplicates = validate_invoices([invoice])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_missing_invoice_id(self):
        invoice = self.invoice.copy()
        invoice["invoice_id"] = ""

        valid, invalid, duplicates = validate_invoices([invoice])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_none_values(self):
        invoice = self.invoice.copy()
        invoice["customer_name"] = None
        invoice["amount"] = None

        valid, invalid, duplicates = validate_invoices([invoice])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_non_numeric_amount(self):
        invoice = self.invoice.copy()
        invoice["amount"] = "abc"

        valid, invalid, duplicates = validate_invoices([invoice])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_duplicate_after_invalid_invoice(self):
        invoice1 = self.invoice.copy()
        invoice1["amount"] = "-500"

        invoice2 = self.invoice.copy()

        valid, invalid, duplicates = validate_invoices(
            [invoice1, invoice2]
        )

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)
        self.assertEqual(len(duplicates), 1)


if __name__ == "__main__":
    unittest.main()
