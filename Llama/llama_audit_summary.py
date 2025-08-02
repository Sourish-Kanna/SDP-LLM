from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import json
import os

class LlamaAuditSummarizer:
    def __init__(self, model: str = "llama3-8b-8192", temperature: float = 0.5):
        load_dotenv()
        self.chat = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")  # type: ignore
        )  # type: ignore

        self.system_prompt = """
You are a multi-role financial auditing assistant. Given structured audit data (including fuzzy insights), your goal is to provide concise, actionable markdown summaries from the perspectives of three key stakeholders.

Analyze the audit JSON with professional judgment and reason about possible implications, patterns, or anomalies.

Return your output strictly in **Markdown** format with the following sections:

##  Legal Summary
- Identify missing or malformed legal fields (e.g., missing GSTIN, invalid invoice dates).
- Highlight any legal non-compliance, risky vendors, or out-of-scope transactions.
- Suggest improvements to meet regulatory and tax obligations.

##  Manager Summary
- Summarize vendor risks (e.g., over-reliance, unusual volume patterns).
- Comment on frequent or large item purchases and their implications.
- Recommend managerial actions (e.g., vendor diversification, spend audits).

##  Accountant Summary
- Confirm whether totals match quantity × unit_price.
- Point out invalid numerical values (zero quantity, negative prices).
- Flag rounding errors, inconsistencies, or unclear line items.
- Offer fixes to ensure clean books.

---

### Additional Instructions:
- Use insights from fuzzy logic or Mistral outputs if available (e.g., vendor patterns, suspicious quantities).
- Keep language clear and professional—suitable for a client or compliance officer.
- Avoid repeating the input JSON; summarize intelligently.
- Use bullet points for clarity and conciseness.
- Focus on actionable insights and recommendations.
- Ensure the output is well-structured and easy to read.
- Do not include any disclaimers or preambles.
- **Do not include any footer or note at the end**.
- Reply as a professional auditor, not as a language model.
- Follow the same structure for each section.
- Use ₹ for currency values.
"""

    def summarize(self, audit_data: dict) -> str:
        """Send audit JSON to LLaMA 3 and return structured markdown summary."""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"{json.dumps(audit_data, indent=2)}")
        ]
        response = self.chat.invoke(messages)
        return response.content  # type: ignore
    
    def chat(self, messages: str) -> str:
        """Send a chat message to the LLaMA model and return the response."""
        print(messages)
        response = self.chat.invoke(messages)
        return response.content

# ✅ Usage Example
if __name__ == "__main__":
    from rich.console import Console
    from rich.markdown import Markdown

    audit_json = {
        "summary": {
            "total_invoices": 2,
            "vendors": 2,
            "date_range": {"start": "2025-06-01", "end": "2025-07-15"}
        },
        "issues": [
            {
                "invoice_id": "INV-1001",
                "vendor": "ABC Traders",
                "issue_type": "total_mismatch",
                "description": "Total does not match quantity × unit_price",
                "severity": "high"
            }
        ],
        "compliance_flags": {
            "future_dates": [{"invoice_id": "INV-1008", "date": "2026-01-01"}],
            "missing_fields": [{"invoice_id": "INV-1001", "field": "GSTIN"}],
            "invalid_gstin": [{"invoice_id": "INV-1002", "gstin": "123INVALIDGST"}]
        },
        "vendor_summary": [
            {"vendor": "ABC Traders", "invoice_count": 10, "total_billed": 500000}
        ],
        "invoice_patterns": {
            "duplicate_amounts": [
                {"amount": 5000, "invoice_ids": ["INV-1005", "INV-1010"]}
            ],
            "repeated_items": [
                {"item": "Widget A", "occurrences": 5}
            ]
        }
    }

    summarizer = LlamaAuditSummarizer()
    markdown_summary = summarizer.summarize(audit_json)
    
    console = Console()
    markdown = Markdown(markdown_summary)
    console.print(markdown)
