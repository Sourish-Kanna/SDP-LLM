import pandas as pd

def parse_csv(file_path):
    """
    Parses a CSV file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The parsed data as a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
        return None

def df_to_invoices(df):
    """
    Converts a DataFrame to a list of invoice dictionaries.

    Args:
    df (pandas.DataFrame): The DataFrame containing invoice data.

    Returns:
    list: A list of dictionaries representing invoices.
    """
    invoices = []
    for _, row in df.iterrows():
        invoice = {
            "invoice_id": row.get("invoice_id"),
            "vendor": row.get("vendor"),
            "date": row.get("date"),
            "quantity": row.get("quantity"),
            "unit_price": row.get("unit_price"),
            "total": row.get("total")
        }
        invoices.append(invoice)
    return invoices

def csv_parser(file_path):
    """
    Parses a CSV file and converts it to a list of invoice dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries representing invoices.
    """
    df = parse_csv(file_path)
    if df is not None:
        return df_to_invoices(df)
    return []

# Example usage:
if __name__ == "__main__":
    import pprint
    invoices = csv_parser('./sample_data/test1.csv')
    pprint.pprint(invoices, indent=2)