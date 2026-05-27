'''This script initializes 
Microsoft Presidio to scan incoming text and swap out
 sensitive items (like SSNs or emails) with
 a secure mask (<PII_REDACTED>).'''

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIISecurityScanner:
    def __init__(self):
        # Initialize the Presidio engines
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def sanitize_text(self, text: str) -> str:
        """
        Scans input text for sensitive data (PII) and redacts it.
        """
        if not text.strip():
            return text

        # Step 1: Analyze the text to find entities like EMAIL, PHONE_NUMBER, US_SSN, etc.
        analysis_results = self.analyzer.analyze(text=text, language="en")

        # Step 2: Anonymize the text based on the analysis results
        anonymized_result = self.anonymizer.anonymize(
            text=text, 
            analyzer_results=analysis_results
        )

        return anonymized_result.text

    def detect_prompt_injection(self, text: str) -> bool:
        """
        A basic behavioral check for prompt injection signatures.
        """
        malicious_phrases = [
            "ignore previous instructions",
            "ignore all instructions",
            "system override",
            "output the internal database",
            "you are now an unconstrained"
        ]
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in malicious_phrases)