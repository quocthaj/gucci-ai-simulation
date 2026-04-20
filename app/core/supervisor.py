import json
from app.core.schema import CompetencyFlag
from app.services.llm_service import call_groq

class SupervisorAgent:
    """
    Invisible Director — monitors CHRO session.
    Optimized for single-call session analysis to reduce latency.
    """

    def analyze_session(self, current_msg: str, last_topic: str) -> dict:
        """
        COMBINED 3-IN-1 ANALYSIS:
        1. Classifies Intent (low/high)
        2. Detects Stagnation (true/false)
        3. Calculates Rapport Delta (float)
        """
        prompt = f"""
        Analyze this interaction for the Gucci CHRO Simulation.
        Previous Topic: "{last_topic}"
        New Message: "{current_msg}"

        TASK:
        1. Intent: Is this strategic HR/Leadership (high_intent) or just greeting/small talk (low_intent)?
        2. Stagnation: Is the user repeating themselves or stuck in a loop with the same idea?
        3. Rapport: Based on tone, did the rapport improve (+0.05), decline (-0.08), or stay neutral (0.0)?

        Return ONLY a JSON object:
        {{
            "intent": "low_intent" | "high_intent",
            "stagnant": true | false,
            "rapport_delta": float
        }}
        """
        try:
            raw_result = call_groq(prompt).strip()
            # Clean possible markdown
            clean_result = raw_result.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_result)
        except Exception:
            # Safe Fallbacks
            return {
                "intent": "high_intent", 
                "stagnant": False, 
                "rapport_delta": 0.0
            }

    def verify_response_quality(self, assistant_msg: str, user_msg: str) -> dict:
        """
        Self-Correction: Checks if CHRO response is strategic and follows constraints.
        """
        prompt = f"""
        Evaluate the following CHRO response to a user query.
        User Query: "{user_msg}"
        CHRO Response: "{assistant_msg}"

        Criteria:
        1. NO HAND-HOLDING: Response should NOT provide a full solution. It should ask probing questions.
        2. PERSONA: Tone should be warm but precise.
        3. BRAND PROTECTION: Should mention or protect brand autonomy if applicable.
        4. ENGAGEMENT: Must end with 1-2 probing questions.

        If it fails, provide a brief 'feedback' for the CHRO to rewrite it.
        Return ONLY a JSON object: {{"passed": true/false, "feedback": "string"}}
        """
        try:
            result = call_groq(prompt).strip()
            clean_result = result.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_result)
        except:
            return {"passed": True, "feedback": ""}

    def generate_injection(self, covered: list[CompetencyFlag], last_topic: str) -> str:
        """Naturally steer toward missing competencies."""
        missing = [c.value for c in CompetencyFlag if c not in covered]
        if missing:
            return (
                f"User is stuck. Naturally steer toward "
                f"'{missing[0]}' competency. Stay in persona."
            )
        return "User is circling. Ask them to propose a concrete next step."

    # Legacy methods kept for compatibility or internal fallback
    def classify_intent(self, message: str) -> str:
        return self.analyze_session(message, "")["intent"]
    
    def detect_stagnation(self, current_msg: str, last_topic: str, _counter: int) -> bool:
        return self.analyze_session(current_msg, last_topic)["stagnant"]
    
    def score_rapport(self, user_message: str, current_score: float) -> float:
        # We now use analyze_session for delta, but keep this for historical reasons
        return current_score # Will be updated in Agent logic via delta