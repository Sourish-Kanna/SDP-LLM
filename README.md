# 📟 Autonomous Audit+ – A Hybrid Agentic Financial Document Auditor

## 🔍 Overview

Autonomous Audit+ is a multi-agent hybrid system that performs intelligent auditing on invoice documents (CSV or PDF). It uses:

* **Mistral 7B via Groq**: For rule-based audit logic (duplicate detection, total mismatch, etc.)
* **LLaMA 3 8B via Groq**: For markdown-formatted summaries, legal/manager/accountant role explanations, and suggestions
* **React Frontend**: For UI/UX, visualizing audit issues, and exporting reports
* **FastAPI Backend**: For file processing, audit orchestration, and serving frontend endpoints

---

## 👥 Team Roles

Here’s how **Prem’s role** in the **Mistral audit logic** can be split across the three simulated agent roles: **Legal**, **Manager**, and **Accountant**. Each sub-role corresponds to a part of the audit logic implemented as LangChain tools.

---

## 👤 **Prem – Mistral + Audit Logic**

### ⚖️ Legal Agent Logic

Prem is responsible for implementing tools and rules that simulate legal and compliance checks:

* ✅ Check **GST compliance** (e.g., GST% must be 5%, 12%, or 18%)
* ✅ Validate **GSTIN format** (15-character alphanumeric)
* ✅ Flag invoices with **future dates**
* ✅ Identify **missing legal fields** (like vendor name or invoice ID)

---

### 👔 Manager Agent Logic

Prem builds logic to simulate the financial oversight of a manager:

* ✅ Detect **vendor concentration** (one vendor dominates total billing)
* ✅ Flag **high-value invoices** or frequent identical amounts
* ✅ Aggregate **total spending per vendor**
* ✅ Identify **repeated patterns** (same items, prices)

---

### 🧮 Accountant Agent Logic

Prem creates fine-grained financial validation tools:

* ✅ Detect **total mismatch**: `total ≠ quantity × unit_price`
* ✅ Identify **missing fields** in numeric columns (quantity, unit\_price)
* ✅ Flag **zero or negative values**
* ✅ Ensure all invoices are **numerically consistent**

---

### ↺ Integration

Prem will:

* Implement all the above checks using LangChain tools
* Chain them inside a Mistral-powered agent using RAG
* Return structured output JSON
* Parses incoming CSV/PDF (after receiving from frontend)
* Generates document embeddings for RAG
* Sets up Mistral 7B + Groq agent
* Returns audit JSON summary to Sourish/frontend

## 👤 **Sourish – LLaMA 3 + Summary Generator**

Here’s how Sourish’s work maps to the three roles used in LLaMA prompting:

### ⚖️ Legal Role (Prompt Design)

* 📜 Craft prompts asking for legal compliance issues based on audit JSON
* 🧠 Ask LLaMA to identify missing fields like GST, invoice format, future dates

### 👔 Manager Role (Prompt Design)

* 📊 Request financial oversight comments: overbilling patterns, large invoices, vendor risk
* 🧠 Ask LLaMA to suggest business improvements or controls

### 🧮 Accountant Role (Prompt Design)

* 🔍 Ask LLaMA to verify totals, identify calculation errors, zero values

* ✏️ Summarize per-invoice anomalies in clear English

* Receives audit output (JSON) from Prem

* Sends prompt to LLaMA 3 via Groq for:

  * Summary generation
  * Role-based analysis (Legal, Manager, Accountant)
  * Suggestions for future prevention

* Formats LLaMA 3 output into:

  * Markdown (for frontend display)
  * PDF (optional)

* Collaborates with Parth to render outputs in UI

## 👤 **Parth – Frontend (React)**

Parth’s UI displays outputs aligned with each expert role:

### ⚖️ Legal View

* 📜 Render missing GST fields, invalid GSTINs, and date flags
* ⚠️ Show legal risk badges or highlights in UI

### 👔 Manager View

* 📊 Display spending distribution, vendor risk, frequent invoice patterns
* 📈 Include bar charts / graphs for visual summaries

### 🧲 Accountant View

* 🧲 Highlight mismatched totals or zero values directly in invoice table

* ✅ Show green checks for verified fields

* Builds UI for:

  * Invoice upload (CSV/PDF)
  * Audit result visualization
  * Role-based explanations (as cards or tabs)
  * Export/download report (PDF or Markdown)

* Calls FastAPI endpoints for audit and summary

* Displays errors using icons/highlights (e.g., red rows, warnings)

* Adds charts using Recharts or Chart.js (vendor totals, error counts)

---

## 📁 Project File Structure

```text
Frontend/               # React-based frontend UI (Parth)
Backend/                # FastAPI backend for coordination (Sourish)
Parser/                 # File input and parsing logic (Sourish)
├── Csv parser.py
└── PDF Parser.py
sample_data/            # Sample CSV and PDF invoices for testing
Llama/                  # Summary generation and prompt logic (Sourish)
Mistal/                 # Audit tools and rule-based logic (Prem)
Readme.md               # Project documentation
Requirments.txt         # Python dependencies
test.py                 # Python test file
```

---

## ↻ Flow Summary

```mermaid
A[User Uploads Invoice File<br>(CSV or PDF) - React UI] --> B[FastAPI Backend<br>(Parse & Normalize - Sourish)]
B --> C[Mistral Audit - Prem<br>(Validation & RAG Agent)]
C --> D[Audit JSON Output]
D --> E[LLaMA 3 Prompting - Sourish<br>(Summary, Roles, Suggestions)]
E --> F[Markdown / PDF Report]
F --> G[React UI - Parth<br>(Render Cards, Tables, Charts)]
```

---

## 🧪 Generalized JSON Input Format (to Mistral)

```json
[
  {
    "invoice_id": "INV-XXXX",
    "date": "YYYY-MM-DD",
    "vendor": "Vendor Name",
    "products": [
      {
        "name": "Item Name",
        "quantity": 0.0,
        "unit_price": 0.0,
        "total": 0.0
      }
    ]
  }
]
```

* Each `products[]` entry represents one line item per invoice.
* Fields should be validated and parsed by the backend before sending to Mistral.

---

## 📅 Generalized JSON Output Format (from Mistral)

```json
{
  "summary": {
    "total_invoices": 0,
    "vendors": 0,
    "date_range": {
      "start": "YYYY-MM-DD",
      "end": "YYYY-MM-DD"
    }
  },
  "issues": [
    {
      "invoice_id": "string",
      "vendor": "string",
      "issue_type": "string",
      "description": "string",
      "severity": "low | medium | high"
    }
  ],
  "compliance_flags": {
    "future_dates": [ { "invoice_id": "string", "date": "YYYY-MM-DD" } ],
    "missing_fields": [ { "invoice_id": "string", "field": "string" } ],
    "invalid_gstin": [ { "invoice_id": "string", "gstin": "string" } ]
  },
  "vendor_summary": [
    {
      "vendor": "string",
      "invoice_count": 0,
      "total_billed": 0.0
    }
  ],
  "invoice_patterns": {
    "duplicate_amounts": [ { "amount": 0.0, "invoice_ids": ["string"] } ],
    "repeated_items": [ { "item": "string", "occurrences": 0 } ]
  }
}
```

* This structure ensures full compatibility with markdown summaries and role-based prompts for LLaMA 3.
* Fields are grouped to support modular display by Legal, Manager, and Accountant views.
