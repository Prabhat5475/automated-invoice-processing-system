
from datetime import datetime


def validate_invoices(invoices):
    valid_invoices = []
    invalid_invoices = []
    duplicate_invoices = []

    seen_ids = set()

    for invoice in invoices:
        errors = []

        invoice_id = invoice["invoice_id"].strip()

        # Check duplicate invoice IDs
        if invoice_id and invoice_id in seen_ids:
            duplicate_invoices.append(invoice)
            continue

        if invoice_id:
            seen_ids.add(invoice_id)

        # Check required fields
        if not invoice_id:
            errors.append("Missing invoice ID")

        if not invoice["customer_name"].strip():
            errors.append("Missing customer name")

        # Validate invoice date
        try:
            datetime.strptime(invoice["invoice_date"], "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid invoice date")

        # Validate amount
        try:
            amount = float(invoice["amount"])
            if amount <= 0:
                errors.append("Amount must be positive")
        except ValueError:
            errors.append("Invalid amount")

        # Validate payment status
        if invoice["status"].strip().upper() not in ["PAID", "PENDING"]:
            errors.append("Invalid payment status")

        if errors:
            invalid_invoices.append({
                "invoice": invoice,
                "errors": errors
            })
        else:
            valid_invoices.append(invoice)

    return valid_invoices, invalid_invoices, duplicate_invoices
