
import pandas as pd
import re


def parse_pdf(file_path):
    """
    Parses a PDF file and extracts text content into a dictionary.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        dict: Dictionary with page numbers as keys and extracted text as values.
    """
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF parsing. Please install it.")

    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        data = {}
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            data[i + 1] = text
    return data

def df_to_invoices(data_dict):
    """
    Converts a dictionary of page texts to a list of invoice dictionaries.
    Extracts invoice fields and line items from each page's text.

    Args:
        data_dict (dict): Dictionary with page numbers as keys and extracted text as values.

    Returns:
        list: A list of invoice dictionaries, each with a list of products.
    """

    invoices = []
    for page_num, text in data_dict.items():
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        invoice_id = None
        date = None
        vendor = None

        # Extract header fields
        for line in lines:
            if line.startswith("Invoice ID:"):
                invoice_id = line.split("Invoice ID:")[1].strip()
            elif line.startswith("Date:"):
                date = line.split("Date:")[1].strip()
            elif line.startswith("Vendor:"):
                vendor = line.split("Vendor:")[1].strip()

        # Find the start of the items table
        try:
            prod_idx = lines.index("Product")
            # The next three lines are headers: Product, Qty, Unit Price, Total
            item_lines = lines[prod_idx + 4:]
            products = []
            # Items are in groups of 4 lines: name, qty, unit price, total
            for i in range(0, len(item_lines), 4):
                if i + 3 < len(item_lines):
                    name = item_lines[i]
                    quantity = item_lines[i + 1]
                    unit_price = item_lines[i + 2]
                    total = item_lines[i + 3]
                    # Stop if we reach "Grand Total"
                    if name.startswith("Grand Total"):
                        break
                    product = {
                        "name": name,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total": total
                    }
                    products.append(product)
            if invoice_id or products:
                invoice = {
                    "invoice_id": invoice_id,
                    "vendor": vendor,
                    "date": date,
                    "products": products
                }
                invoices.append(invoice)
        except ValueError:
            pass  # No product table found

    return invoices



if __name__ == "__main__":
    import pprint
    pdf_text = parse_pdf('sample_data/mul_1.pdf')
    # pprint.pprint(pdf_text)  # Display all extracted text
    invoices = df_to_invoices(pdf_text)
    pprint.pprint(invoices)  # Display all invoices