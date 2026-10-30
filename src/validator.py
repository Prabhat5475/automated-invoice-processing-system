
from datetime import datetime


def validate_invoices(invoices):
    valid_invoices = []
    invalid_invoices = []
    duplicate_invoices = []

    seen_ids = set()

    for invoice in invoices:
        errors = []

        invoice_id = (invoice.get("invoice_id") or "").strip()
        customer_name = (invoice.get("customer_name") or "").strip()
        invoice_date = (invoice.get("invoice_date") or "").strip()
        amount_value = (invoice.get("amount") or "").strip()
        status = (invoice.get("status") or "").strip().upper()

        # Check duplicate invoice IDs
        if invoice_id and invoice_id in seen_ids:
            duplicate_invoices.append(invoice)
            continue

        if invoice_id:
            seen_ids.add(invoice_id)

        # Check required fields
        if not invoice_id:
            errors.append("Missing invoice ID")

        if not customer_name:
            errors.append("Missing customer name")

        # Validate invoice date
        try:
            datetime.strptime(invoice_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid invoice date")

        # Validate amount
        try:
            amount = float(amount_value)

            if amount <= 0:
                errors.append("Amount must be positive")

        except (ValueError, TypeError):
            errors.append("Invalid amount")

        # Validate payment status
        if status not in ["PAID", "PENDING"]:
            errors.append("Invalid payment status")

        if errors:
            invalid_invoices.append({
                "invoice": invoice,
                "errors": errors
            })
        else:
            valid_invoices.append(invoice)

    return valid_invoices, invalid_invoices, duplicate_invoices
