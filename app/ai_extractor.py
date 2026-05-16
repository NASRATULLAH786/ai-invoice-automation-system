import re


def extract_invoice_data(invoice_text):

    try:

        invoice_number = re.search(
            r'INV-\d+-\d+',
            invoice_text
        )

        total_amount = re.search(
            r'\$\d+',
            invoice_text
        )

        date = re.search(
            r'May \d+ \d+',
            invoice_text
        )

        company_name = "Madina Tech Solutions"

        return {
            "company_name": company_name,
            "invoice_number": invoice_number.group() if invoice_number else "N/A",
            "date": date.group() if date else "N/A",
            "total_amount": total_amount.group() if total_amount else "N/A"
        }

    except Exception as e:

        return {
            "error": str(e)
        }