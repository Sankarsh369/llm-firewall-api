import re

class InjectionDetector:
    def __init__(self):
        # We look for common attack vectors, obfuscations, and context-hijacking attempts
        self.risk_patterns = [
            r"ignore\s+previous\s+instructions",         # Classic system override
            r"disregard\s+the\s+system\s+prompt",        # Instructional inversion
            r"base64",                                   # Encoded payloads
            r"forget\s+everything",                      # Context hijacking
            r"pretend\s+you\s+are\s+[a-z]+",             # Role-playing exploits (e.g., DAN)
            r"system\s+override",                        # System override commands
            r"do\s+not\s+say\s+the\s+secret\s+word",     # Reverse psychology
            r"tell\s+me\s+the\s+password",               # Direct data extraction
            r"bypass\s+content\s+filters"                # Direct bypass requests
        ]
        
        # Compile regex for blazing fast execution
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.risk_patterns]

    def analyze_prompt(self, user_prompt: str) -> dict:
        """
        Scans the incoming text for malicious intent and calculates a threat score.
        """
        threat_score = 0
        triggered_rules = []

        # 1. Check against known malicious patterns
        for pattern in self.compiled_patterns:
            if pattern.search(user_prompt):
                threat_score += 0.4  # Add 40% risk for every matched pattern
                triggered_rules.append(pattern.pattern)

        # 2. Check for suspicious formatting (Encoding & Capitalization Tricks)
        # Hackers use unconventional capitalization like "iGnOrE aLl PrEvIoUs InStRuCtIoNs"
        if self._detect_mixed_casing(user_prompt):
            threat_score += 0.2
            triggered_rules.append("suspicious_mixed_casing")

        # Cap the score at 1.0 (100% certainty)
        final_score = min(threat_score, 1.0)
        
        return {
            "is_safe": final_score < 0.5,  # If score is 50% or higher, we block it
            "threat_score": final_score,
            "flagged_patterns": triggered_rules
        }

    def _detect_mixed_casing(self, text: str) -> bool:
        """Detects if a user is trying to bypass basic filters with AlTeRnAtInG caps."""
        if len(text) < 10:
            return False
        
        # Count alternating case transitions
        transitions = sum(1 for i in range(len(text)-1) if text[i].isalpha() and text[i+1].isalpha() and text[i].islower() != text[i+1].islower())
        
        # If more than 30% of the text is alternating cases, it is highly suspicious
        return transitions / len(text) > 0.3

# Create a singleton instance we can use across our API
detector = InjectionDetector()