import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Define the exact JSON structure we want back from the cloud LLM
class LLMAnalysisResult(BaseModel):
    intent_category: str = Field(description="The primary category of the prompt (e.g., Coding, Data Analytics, General, Malicious)")
    risk_score_out_of_ten: int = Field(description="Safety risk score from 1 to 10 based on content safety.")
    summary: str = Field(description="A concise 1-sentence summary of what the user is requesting.")

class LLMOpsAnalyzer:
    def __init__(self):
        # Initializes the client using the GEMINI_API_KEY environment variable automatically
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client() if api_key else None

    def analyze_log_context(self, user_prompt: str) -> dict:
        """
        Sends the user prompt to Gemini in the cloud and enforces a structured JSON response.
        """
        # Fallback if no API key is provided yet
        if not self.client:
            return {"intent_category": "Unknown", "risk_score_out_of_ten": 1, "summary": "API Key Missing"}

        system_instruction = (
            "You are an advanced security auditing agent. Analyze the user's prompt "
            "and categorize its intent, score its risk level, and summarize it."
        )

        try:
            # We call gemini-2.5-flash as it is lightning fast and free-tier optimized
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    # This parameter forces the model to respond ONLY in our strict schema format
                    response_mime_type="application/json",
                    response_schema=LLMAnalysisResult,
                    temperature=0.1 # Low temperature ensures deterministic, reliable outputs
                ),
            )
            
            # The response text is guaranteed to be a valid JSON string matching our schema
            return json.loads(response.text)

        except Exception as e:
            print(f"[LLMOps Error]: Cloud API request failed: {e}")
            # Fallback data structure so the pipeline doesn't crash on network errors
            return {
                "intent_category": "Error/Timeout",
                "risk_score_out_of_ten": 0,
                "summary": "Failed to contact cloud LLMOps provider."
            }