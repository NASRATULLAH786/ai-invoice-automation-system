import re


def extract_invoice_data(invoice_text):
    try:

        # Company Name
        company_match = re.search(
            r'Company\s*:\s*(.+)',
            invoice_text,
            re.IGNORECASE
        )

        # Invoice Number
        invoice_match = re.search(
            r'Invoice\s*Number\s*:\s*([A-Z0-9\-]+)',
            invoice_text,
            re.IGNORECASE
        )

        # Date
        date_match = re.search(
            r'Date\s*:\s*([\d\-\/]+)',
            invoice_text,
            re.IGNORECASE
        )

        # Total Amount
        amount_match = re.search(
            r'Total\s*(Amount)?\s*:\s*\$?([\d,.]+)',
            invoice_text,
            re.IGNORECASE
        )

        return {
            "company_name": company_match.group(1).strip() if company_match else "N/A",

            "invoice_number": invoice_match.group(1).strip() if invoice_match else "N/A",

            "date": date_match.group(1).strip() if date_match else "N/A",

            "total_amount": amount_match.group(2).strip() if amount_match else "N/A"
        }

    except Exception as e:
        return {
            "error": str(e)
        }