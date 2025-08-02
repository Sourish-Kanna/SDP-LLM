import json
import re
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
# Make sure this import path matches your project structure
from Mistral.audit_logic import MistralAuditLogic 

class InvoiceAuditAgent:
    """
    A refined agent that performs a rule-based audit and then uses an LLM
    for fuzzy insights in a secure and reliable way.
    """
    def __init__(self, model: str = "qwen/qwen3-32b", temperature: float = 0.2):
        load_dotenv()
        self.chat = ChatGroq(
            model=model,
            temperature=temperature,
        )
        self.prompt_template = PromptTemplate(
            input_variables=["audit_json"],
            template=self._load_template(),
        )
        self.chain = self.prompt_template | self.chat

    def _load_template(self) -> str:
        # This template is well-defined and requires no changes.
        return ("""
You are an AI Auditor powered by the Qwen model.
You receive invoice audit JSON and your job is to add fuzzy insights using general reasoning:

- Is the item mix unusual?
- Are quantities suspicious?
- Are there vendors with only one invoice?
- Are any items zero quantity or zero billed?
- Do repeated amounts or frequent items show patterns?

Only return valid JSON like this:

  "fuzzy_insights": [
    { "type": "suspicious_quantity", "description": "..." },
    { "type": "vendor_pattern", "description": "..." }
  ]

Do not return any other text or explanations, just the JSON.
Do not return any other keys, just the "fuzzy_insights" key.
Do not include ``` and json at the start or end of your response.

Input JSON:
{audit_json}""")

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Safely extracts a JSON object from a string, even if it's wrapped in text or code blocks.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON object found in the response.")
        
        # Use safe json.loads() instead of insecure eval()
        return json.loads(match.group())

    def audit(self, invoice_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        mistral_logic = MistralAuditLogic(invoice_data)
        audit_json = mistral_logic.run_audit()
        
        try:
            # Pass the audit data as a well-formed JSON string to the model
            input_for_llm = json.dumps(audit_json, indent=2)
            response = self.chain.invoke({"audit_json": input_for_llm})
            
            # Safely parse the response content
            fuzzy = self._extract_json(response.content)
            
            audit_json.update({"fuzzy_insights": fuzzy.get("fuzzy_insights", [])})
            
        except (json.JSONDecodeError, ValueError, Exception) as e:
            # Return a simple, serializable error message
            print(f"❌ Failed to get or parse fuzzy insights: {e}")
            audit_json.update({
                "fuzzy_insights_error": "Failed to generate or parse insights from the model.",
            })
            
        return audit_json