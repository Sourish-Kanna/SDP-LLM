# 📟 Autonomous Audit+ – A Hybrid Agentic Financial Document Auditor

## 🔍 Overview

Autonomous Audit+ is a hybrid multi-agent invoice auditing system that combines rule-based logic with natural language understanding. It processes both CSV and PDF invoices to:

* Detect financial issues
* Generate plain-English explanations

The system uses:

* **Mistral 7B via Groq + LangChain** for rule-based and RAG audit logic
* **Gemini 1.5 Pro** for fluent summaries and suggestions
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
  * Suggestions
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

```text
invoice_audit_agent/
├── app.py                    # Streamlit app UI
├── embeddings/               # Embedding logic 
│   ├── vector_store.py
│   └── retriever_utils.py
├── parsers/                  # PDF/CSV handling 
│   ├── csv_parser.py
│   └── pdf_parser.py
├── reports/                  # Gemini prompt + writer 
│   └── gemini_writer.py
├── audit/                    # Mistral logic 
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

### ✅ Initial Normalized DataFrame (After Parsing CSV/PDF)

| Field       | Type                |
| ----------- | ------------------- |
| invoice\_id | string              |
| vendor      | string              |
| date        | string (YYYY-MM-DD) |
| quantity    | float               |
| unit\_price | float               |
| total       | float               |

This is parsed from CSV or PDF, and passed to:

* Vector embedder (you)
* Mistral audit agent (teammate)

---

### 🔄 Intermediate Format to Mistral (Shared Input)

```json
{
  "invoices": [
    {
      "invoice_id": "INV-101",
      "vendor": "ABC Traders",
      "date": "2025-01-23",
      "quantity": 250,
      "unit_price": 110.0,
      "total": 27500.0
    },
    ...
  ]
}
```

* This structure is passed from **you to your teammate**.
* Also stored in vector DB by you.

---

### 📉 Output Format from Mistral to You (for Gemini)

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
  "compliance_flags": {
    "gst_issues": 3,
    "future_dates": 1
  },
  "top_vendors": [
    { "name": "ABC Traders", "amount_billed": 18500 }
  ]
}
```

* Returned from **Mistral agent to you**
* You use this for Gemini summaries and markdown report generation

---

## 🗓️ Development Timeline

| Day | Task                                   |
| --- | -------------------------------------- |
| 1   | UI + file upload                       |
| 2   | File parsing + cleaning                |
| 3   | Audit rule logic (mistral)             |
| 4   | LangChain agent setup                  |
| 5   | Gemini summary generation              |
| 6   | Role-based agent views                 |
| 7   | Duplicate detection (cross-invoice)    |
| 8   | Charting and final audit summary       |
| 9   | Internal testing                       |
| 10  | Polish, test, and export final reports |

---

> This README serves as the central reference document for planning, development, and integration. Keep it updated as modules evolve.
