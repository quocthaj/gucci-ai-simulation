from app.core.schema import CompetencyFlag, StateUpdate, NPCResponse
from app.core.supervisor import SupervisorAgent
from app.services.llm_service import llm_call


class SlidingWindowMemory:
    """Lightweight replacement for langchain ConversationBufferWindowMemory."""

    def __init__(self, k: int = 6):
        self.k = k
        self._messages: list[dict] = []

    def load_memory_variables(self, _inputs: dict) -> dict:
        return {"history": self._messages[-(self.k * 2):]}

    def save_context(self, inputs: dict, outputs: dict) -> None:
        self._messages.append({"role": "user", "content": inputs["input"]})
        self._messages.append({"role": "assistant", "content": outputs["output"]})


class CHROAgent:
    SYSTEM_PROMPT = """
You are the Chief Human Resources Officer (CHRO) of the Gucci Group.
You are strategically minded, warm but precise, and deeply protective
of each brand's unique identity.

YOUR MANDATE:
Guide the Global OD Director (the User) to design a Group-level
leadership system grounded in four competencies:
Vision, Entrepreneurship, Passion, and Trust.

HARD CONSTRAINTS — never break these:
1. No hand-holding: Never design the system FOR the user.
   Ask probing questions to drive THEIR thinking instead.
2. Protect brand autonomy: Firmly push back on any
   "one-size-fits-all" approach that erases brand DNA.
3. Never discuss compensation bands without CLO sign-off.
4. Stay on scope: If user goes off-topic, redirect to
   the competency framework immediately.

BEHAVIORAL RULES:
- Always ask 1-2 clarifying questions before giving direction.
- If user is vague, name which competency they should anchor to.
- If user seems stuck or repeating themselves, challenge them
  with a harder question rather than giving the answer.

CRITICAL: The "Current session state" block above is your 
internal context only. NEVER repeat, quote, or reference 
it in your response to the user.

LANGUAGE RULE:
- Detect the user's language automatically.
- Always respond in the same language the user used.

RESPONSE LENGTH RULE:
- Keep every response under 120 words maximum.
- Ask maximum 2 probing questions per turn, never more.
- No long preamble — get to the point within 1 sentence.
 
Current session state: {state_context}
{supervisor_injection}
"""

    def __init__(self, persona_id: str, session_id: str):
        self.persona_id = persona_id
        self.session_id = session_id
        self.state = StateUpdate()
        self.memory = SlidingWindowMemory(k=6)
        self.supervisor = SupervisorAgent()

    def _build_system_prompt(self, injection: str | None = None) -> str:
        tone_note = ""
        if self.state.rapport_score < 0.3:
            tone_note = "Adopt a more formal and guarded tone."
        elif self.state.rapport_score > 0.7:
            tone_note = "You may be more candid and collaborative."
        else:
            tone_note = "Maintain warm but precise tone."

        state_context = (
        f"Tone: {tone_note} | "
        f"Competencies discussed so far: "
        f"{[c.value for c in self.state.competencies_covered]} | "
        f"Stagnation level: {self.state.stagnation_counter}/3"
    )
        supervisor_injection = f"\n[DIRECTOR]: {injection}" if injection else ""
        return self.SYSTEM_PROMPT.format(
        state_context=state_context,
        supervisor_injection=supervisor_injection
    )
    COMPETENCY_KEYWORDS = {
    CompetencyFlag.VISION: [
        "vision", "tầm nhìn", "strategic", "chiến lược", "direction", "định hướng"
    ],
    CompetencyFlag.ENTREPRENEURSHIP: [
        "entrepreneurship", "tinh thần khởi nghiệp", "innovation", 
        "đổi mới", "risk", "rủi ro", "ownership"
    ],
    CompetencyFlag.PASSION: [
        "passion", "đam mê", "commitment", "cam kết", 
        "enthusiasm", "nhiệt huyết", "craft", "nghề"
    ],
    CompetencyFlag.TRUST: [
        "trust", "tin tưởng", "transparency", "minh bạch", 
        "integrity", "liêm chính", "reliability"
    ],
}

    def _update_state(self, user_message: str, response: str | None = None) -> None:
        msg = user_message.lower()
        if len(user_message.split()) >= 15:
            for comp, keywords in self.COMPETENCY_KEYWORDS.items():
                if any(kw in msg for kw in keywords):
                    if comp not in self.state.competencies_covered:
                        self.state.competencies_covered.append(comp)

        is_stagnant = self.supervisor.detect_stagnation(
            current_msg=user_message,
            last_topic=self.state.last_topic,
            counter=self.state.stagnation_counter
        )
        self.state.stagnation_counter = (
        self.state.stagnation_counter + 1 if is_stagnant else 0
    )
        self.state.rapport_score = self.supervisor.score_rapport(
            user_message, self.state.rapport_score
        )
        self.state.last_topic = user_message[:80]

    def _check_safety(self, user_message: str) -> list[str]:
        flags = []
        blocked = ["salary bands", "compensation range", "pay grade"]
        if any(t in user_message.lower() for t in blocked):
            flags.append("comp_band_restricted")
        if len(user_message.strip()) < 10:
            flags.append("low_quality_input")
        return flags

    def run(self, user_message: str) -> NPCResponse:
        safety_flags = self._check_safety(user_message)
        injection = None
        if self.state.stagnation_counter >= 3:
            injection = self.supervisor.generate_injection(
                covered=self.state.competencies_covered,
                last_topic=self.state.last_topic
            )
            self.state.injection_fired = True

        system_prompt = self._build_system_prompt(injection)
        history = self.memory.load_memory_variables({}).get("history", [])

        response = llm_call(
            system=system_prompt,
            history=history,
            user_message=user_message
        )

        self.memory.save_context(
            {"input": user_message},
            {"output": response}
        )
        self._update_state(user_message, response)

        return NPCResponse(
            assistant_message=response,
            state_update=self.state,
            safety_flags=safety_flags
        )