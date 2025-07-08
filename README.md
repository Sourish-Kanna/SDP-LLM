# 🧾 Autonomous Audit+ – A Hybrid Agentic Financial Document Auditor

## 🔍 Overview

Autonomous Audit+ is a hybrid multi-agent invoice auditing system that combines rule-based logic with natural language understanding. It processes both CSV and PDF invoices to:

* Detect financial issues
* Generate plain-English explanations
* Answer natural language questions
* Output risk-scored reports

The system uses:

* **Mistral 7B via Groq + LangChain** for rule-based and RAG audit logic
* **Gemini 1.5 Pro** for fluent summaries, suggestions, and Q\&A
* **Streamlit** as the UI frontend

---

## 👥 Team Role Breakdown

### 👤 You (Gemini + Input / Embeddings)

* CSV and PDF file parsing
* Normalizing data into a unified DataFrame
* Chunking and embedding documents using LangChain-compatible vector store
* Generating Gemini prompts for:

  * Audit summary
  * Multi-agent role simulation (accountant, legal, manager)
  * Suggestions and Q\&A
* Exporting markdown/PDF reports

### 👤 Teammate (Mistral + Audit Logic)

* Build LangChain tools for audit rules:

  * Total mismatch
  * Missing fields
  * Duplicate invoice IDs
  * Future dates
* Set up Mistral via Groq in LangChain agent
* Integrate with retriever provided by you
* Implement RAG (Retrieval-Augmented Generation) chains
* Output structured JSON for Gemini processing

---

## 📁 Folder Structure

``` text
invoice_audit_agent/
├── app.py                    # Streamlit app UI
├── embeddings/               # Embedding logic (you)
│   ├── vector_store.py
│   └── retriever_utils.py
├── parsers/                  # PDF/CSV handling (you)
│   ├── csv_parser.py
│   └── pdf_parser.py
├── reports/                  # Gemini prompt + writer (you)
│   └── gemini_writer.py
├── audit/                    # Mistral logic (teammate)
│   ├── audit_tools.py
│   ├── audit_agent.py
│   └── rag_agent.py
├── utils/
│   └── formatter.py          # Shared helpers
├── sample_data/              # Test files
├── requirements.txt          # Dependencies
└── .env                      # Secrets/API keys
```

---

## 📄 File Format Guidelines

### ✅ Expected Fields (CSV or Extracted from PDF)

| Field        | Required | Example         |
| ------------ | -------- | --------------- |
| invoice\_id  | ✅        | INV-1024        |
| vendor       | ✅        | ABC Traders     |
| date         | ✅        | 2025-01-23      |
| quantity     | ✅        | 250             |
| unit\_price  | ✅        | 110.0           |
| total        | ✅        | 27500.0         |
| gst\_number  | Optional | 27AACCA8432H1ZQ |
| gst\_percent | Optional | 18.0            |
| amount\_paid | Optional | 15000.0         |
| discount     | Optional | 8662.5          |

### 📄 PDF Support

* Must be text-based, not scanned image
* Multi-page invoices supported
* Extracted using `pdfplumber` with regex + fallback table parse

---

## 🧾 Output JSON (From Mistral Agent)

```json
{
  "invoice_summary": {
    "total_invoices": 12,
    "files_processed": ["jan.csv", "feb.pdf"]
  },
  "issues": [
    {
      "invoice_id": "INV-1024",
      "vendor": "ABC Traders",
      "issue_type": "Total Mismatch",
      "description": "Total does not match quantity x unit price",
      "severity": "high"
    }
  ],
  "risk_score": {
    "score": 7.5,
    "scale": "out_of_10",
    "risk_level": "high"
  },
  "compliance_flags": {
    "gst_issues": 3,
    "future_dates": 1
  },
  "top_vendors": [
    { "name": "ABC Traders", "amount_billed": 18500 }
  ]
}
```

---

<!-- ## 🗓️ Development Timeline

| Day | Task                                   |
| --- | -------------------------------------- |
| 1   | UI + file upload                       |
| 2   | File parsing + cleaning                |
| 3   | Audit rule logic (mistral)             |
| 4   | LangChain agent setup                  |
| 5   | Gemini summary generation              |
| 6   | Role-based agent views                 |
| 7   | Duplicate detection (cross-invoice)    |
| 8   | Risk scoring + charting                |
| 9   | Q\&A interface                         |
| 10  | Polish, test, and export final reports |

--- -->

## 🚀 Next Steps

* [ ] Finalize file input format and validators
* [ ] Complete PDF parser to support multipage
* [ ] Build vector store and share retriever
* [ ] Mistral agent integration with tools
* [ ] Gemini prompt chaining and report writing

<!-- --- -->
