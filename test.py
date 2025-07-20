
from parsers.csv_parser import csv_parser
from parsers.pdf_parser import pdf_parser
from Llama.llama_audit_summary import LlamaAuditSummarizer
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

def print_and_summarize(invoices, parser_name):
    print(f"\n--- {parser_name} Output ---")
    for inv in invoices:
        print(inv)
    if invoices:
        summarizer = LlamaAuditSummarizer()
        summary = summarizer.summarize({"invoices": invoices})
        console = Console()
        markdown_summary = f"\n--- Llama Summary for {parser_name} ---\n{summary}"
        markdown = Markdown(markdown_summary)
        console.print(markdown)

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    csv_invoices = csv_parser('./sample_data/test1.csv')
    print_and_summarize(csv_invoices, "CSV Parser")

    pdf_invoices = pdf_parser('./sample_data/mul_1.pdf')
    print_and_summarize(pdf_invoices, "PDF Parser")
