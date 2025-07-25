from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
from Mistral.audit_logic import MistralAuditLogic

class InvoiceAuditAgent:
    def __init__(self, model: str = "mistral-saba-24b", temperature: float = 0.2):
        load_dotenv()
        self.chat = ChatGroq(
            model=model,
            temperature=temperature,
        ) # type: ignore
        self.prompt_template = PromptTemplate(
            input_variables=["audit_json"],
            template=self._load_template(),
        )
        self.chain = self.chain = self.prompt_template | self.chat

    def _load_template(self) -> str:
      return ("""
You are an AI Auditor powered by the Mistral model.
You receive invoice audit JSON and your job is to add fuzzy insights using general reasoning:

- Is the item mix unusual?
- Are quantities suspicious?
- Are there vendors with only one invoice?
- Are any items zero quantity or zero billed?
- Do repeated amounts or frequent items show patterns?

Only return valid JSON like this:

  "fuzzy_insights": [
    {{ "type": "suspicious_quantity", "description": "..." }},
    {{ "type": "vendor_pattern", "description": "..." }}
  ]

Do not return any other text or explanations, just the JSON.
Do not return any other keys, just the "fuzzy_insights" key.
Do not include ``` and json at the start or end of your response.

Input JSON:
{{ audit_json }}""")


    def audit(self, invoice_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        mistral_logic = MistralAuditLogic(invoice_data)
        audit_json = mistral_logic.run_audit()
        # print("Audit JSON:", audit_json)
        response = self.chain.invoke({"audit_json": audit_json})
        # print(f"Raw response from model: {[response.content]}")
        try:
            # print(response.content.replace("```", "").split("json")[1]) # type: ignore
            fuzzy = eval(response.content.replace("```", "").split("json")[1]) # type: ignore
            audit_json.update({"fuzzy_insights": fuzzy.get("fuzzy_insights", [])})
            # print("With fuzzy insights:", audit_json)
            return audit_json
        except Exception:
            return {"error": "Invalid JSON from model", "raw_response": response}


if __name__ == "__main__":
    sample_data = [
      { 'date': '2025-06-01',
        'invoice_id': 'INV-1001',
        'products': [ { 'name': 'Cement Bags', 'quantity': '10', 'total': 'Rs. 5000.00', 'unit_price': 'Rs. 500.00'},
                      { 'name': 'Steel Rods', 'quantity': '5', 'total': 'Rs. 6000.00', 'unit_price': 'Rs. 1200.00'}],
        'vendor': 'ABC Traders'},
      { 'date': '2025-08-12',
        'invoice_id': 'INV-1002',
        'products': [ { 'name': 'Bricks', 'quantity': '1000', 'total': 'Rs. 10000.00', 'unit_price': 'Rs. 10.00'},
                      { 'name': 'Sand Bags', 'quantity': '50', 'total': 'Rs. 4000.00', 'unit_price': 'Rs. 80.00'}],
        'vendor': 'XYZ Construction Supplies'},
      { 'date': '2025-06-20',
        'invoice_id': 'INV-1003',
        'products': [ { 'name': 'Pipes (PVC)', 'quantity': '20', 'total': 'Rs. 6000.00', 'unit_price': 'Rs. 300.00'},
                      { 'name': 'Valves', 'quantity': '0', 'total': 'Rs. 0.00', 'unit_price': 'Rs. 150.00'}],
        'vendor': ''},
      { 'date': '2025-07-05',
        'invoice_id': 'INV-1004',
        'products': [ { 'name': 'Paint (White)', 'quantity': '5', 'total': 'Rs. 4000.00', 'unit_price': 'Rs. 800.00'},
                      { 'name': 'Brushes', 'quantity': '20', 'total': 'Rs. 1000.00', 'unit_price': 'Rs. 50.00'},
                      { 'name': 'Rollers', 'quantity': '10', 'total': 'Rs. 750.00', 'unit_price': 'Rs. 75.00'}],
        'vendor': 'Building Solutions Inc.'}
    ]

    agent = InvoiceAuditAgent()
    result = agent.audit(sample_data)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
