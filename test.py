from parsers.csv_parser import csv_parser
from parsers.pdf_parser import pdf_parser
from Llama.llama_audit_summary import LlamaAuditSummarizer
from Mistral.mistral_audit_agent import InvoiceAuditAgent
from rich.console import Console
from rich.markdown import Markdown
import json

def print_and_summarize(raw_invoices, parser_name):
    # print(f"\n--- {parser_name} Parsed Output ---")
    for inv in raw_invoices:
        print(json.dumps(inv, indent=2, ensure_ascii=False))

    if raw_invoices:
        # 🧠 Run through Mistral Agent first
        mistral_agent = InvoiceAuditAgent()
        audit_output = mistral_agent.audit(raw_invoices)
        # print(f"{[audit_output]}")

        # print(f"\n--- Mistral Agent Audit Output ---")
        # print(json.dumps(audit_output, indent=2, ensure_ascii=False))

        # 🦙 Then summarize with LLaMA
        summarizer = LlamaAuditSummarizer()
        summary = summarizer.summarize({"audit_json": audit_output})

        console = Console()
        print(f"\n--- LLaMA Summary for {parser_name} ---\n")
        markdown_summary = f"{summary}"
        markdown = Markdown(markdown_summary)
        console.print(markdown)

if __name__ == "__main__":
    csv_invoices = csv_parser('./sample_data/test1.csv')
    # print_and_summarize(csv_invoices, "CSV Parser")

    # Uncomment to test PDF
    pdf_invoices = pdf_parser('./sample_data/mul_1.pdf')
    # print_and_summarize(pdf_invoices, "PDF Parser")

    list_invoices = csv_invoices + pdf_invoices
    print_and_summarize(list_invoices, "Combined CSV and PDF Parser")