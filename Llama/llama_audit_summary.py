from typing import Any
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
import json


class LlamaAuditSummarizer:
    def __init__(self, model: str = "llama3-8b-8192", temperature: float = 0.5):
        
        self.chat = ChatGroq(
            model=model,
            temperature=temperature,
        ) # type: ignore
        self.prompt_template = PromptTemplate(
            input_variables=["audit_json"],
            template="""
You are a financial auditing assistant. Your task is to analyze structured audit data from three perspectives:

### ⚖️ Legal Expert
- Detect missing legal fields (e.g., GSTIN, invoice ID).
- Flag invalid GSTIN formats and future invoice dates.
- Suggest legal compliance improvements.

### 👔 Financial Manager
- Identify vendor-related risks such as high concentration or frequent large invoices.
- Detect duplicate invoice patterns and repeated items.
- Suggest operational or managerial controls.

### 🧮 Accountant
- Verify numeric consistency, flag mismatches in total vs quantity × unit_price.
- Detect missing or invalid numeric fields (zero or negative values).
- Recommend fixes to ensure accounting accuracy.

Respond **only in Markdown**, structured like this:

```
## ⚖️ Legal Summary
- ...

## 👔 Manager Summary
- ...

## 🧮 Accountant Summary
- ...
```
"""
        )

    def summarize(self, audit_data: dict) -> str:
        """Send audit JSON to LLaMA 3 and return structured markdown summary"""
        messages = [
            SystemMessage(content=self.prompt_template.template),
            HumanMessage(content=f"```json\n{json.dumps(audit_data, indent=2)}\n```")
        ]
        response = self.chat.invoke(messages)
        return response.content # type: ignore


# Usage Example
if __name__ == "__main__":
    from dotenv import load_dotenv
    from rich.console import Console
    from rich.markdown import Markdown

    load_dotenv()

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
