from app.core.schema import CompetencyFlag
from app.services.llm_service import call_groq # Import Groq thay vì thư viện Toán

class SupervisorAgent:
    """
    Invisible Director — monitors CHRO session.
    Uses lightweight LLM classification (Groq) to detect stagnation.
    """

    def classify_intent(self, message: str) -> str:
        """
        Acts as the 'Semantic Router'.
        Classifies message as 'low_intent' (greetings, small talk) or 'high_intent' (HR strategy).
        """
        prompt = f"""
        Classify the following user message: "{message}"
        Options:
        - "low_intent": Greetings, simple thank you, basic acknowledgment, or total gibberish.
        - "high_intent": Questions about HR, leadership, Gucci competencies, feedback systems, or organizational design.
        
        Answer ONLY with the category name.
        """
        result = call_groq(prompt).strip().lower()
        if "high_intent" in result:
            return "high_intent"
        return "low_intent"

    def detect_stagnation(
        self, current_msg: str, last_topic: str, counter: int
    ) -> bool:
        if not last_topic:
            return False
            
        # Nhờ Llama 3 trên Groq check siêu tốc
        prompt = f"""
        User's previous message: "{last_topic}"
        User's current message: "{current_msg}"
        Are they just repeating the exact same core idea without making progress? 
        Answer ONLY with 'yes' or 'no'.
        """
        result = call_groq(prompt).strip().lower()
        return 'yes' in result

    def score_rapport(self, user_message: str, current_score: float) -> float:
        # Giữ nguyên logic tính điểm thái độ của ông
        positive = ["agree", "great", "understood", "exactly", "thanks"]
        negative = ["no", "wrong", "disagree", "that's not", "irrelevant"]
        delta = 0.0
        for w in positive:
            if w in user_message.lower():
                delta += 0.05
        for w in negative:
            if w in user_message.lower():
                delta -= 0.08
        return max(0.0, min(1.0, current_score + delta))

    def generate_injection(
        self, covered: list[CompetencyFlag], last_topic: str
    ) -> str:
        # Giữ nguyên logic tiêm kịch bản của ông
        missing = [c.value for c in CompetencyFlag if c not in covered]
        if missing:
            return (
                f"User is stuck. Naturally steer toward "
                f"'{missing[0]}' competency. Stay in persona."
            )
        return "User is circling. Ask them to propose a concrete next step."