export default function StatePanel({ state, tokenUsage }) {
    const rapport = Math.round(state.rapport_score * 100)
    const competencies = ["vision", "entrepreneurship", "passion", "trust"]

    return (
        <div style={{
            flex: 3,
            background: "#1a1a1a",
            color: "#fff",
            padding: 24,
            display: "flex",
            flexDirection: "column",
            gap: 20,
            overflowY: "auto"
        }}>
            <h3 style={{ color: "#c9a84c", margin: 0 }}>Director Panel</h3>

            {/* Rapport */}
            <div>
                <div style={{ fontSize: 12, color: "#888", marginBottom: 6 }}>Rapport Score</div>
                <div style={{ background: "#333", borderRadius: 8, height: 8 }}>
                    <div style={{
                        width: `${rapport}%`,
                        height: 8,
                        borderRadius: 8,
                        background: rapport > 60 ? "#2ecc71" : rapport > 30 ? "#f39c12" : "#e74c3c",
                        transition: "width 0.5s"
                    }} />
                </div>
                <div style={{ fontSize: 12, color: "#888", marginTop: 4 }}>{rapport}%</div>
            </div>

            {/* Stagnation */}
            <div>
                <div style={{ fontSize: 12, color: "#888", marginBottom: 6 }}>Stagnation Counter</div>
                <div style={{ fontSize: 28, fontWeight: "bold", color: state.stagnation_counter >= 3 ? "#e74c3c" : "#fff" }}>
                    {state.stagnation_counter} / 3
                </div>
                {state.injection_fired && (
                    <div style={{ fontSize: 11, color: "#e74c3c", marginTop: 4 }}>
                        ⚡ Supervisor injected hint
                    </div>
                )}
            </div>

            {/* Competencies */}
            <div>
                <div style={{ fontSize: 12, color: "#888", marginBottom: 8 }}>Competencies Covered</div>
                {competencies.map(c => (
                    <div key={c} style={{
                        display: "flex", alignItems: "center", gap: 8,
                        marginBottom: 6, fontSize: 13
                    }}>
                        <div style={{
                            width: 10, height: 10, borderRadius: "50%",
                            background: state.competencies_covered.includes(c) ? "#2ecc71" : "#444"
                        }} />
                        {c.charAt(0).toUpperCase() + c.slice(1)}
                    </div>
                ))}
            </div>

            {/* Token Usage */}
            {tokenUsage && (
                <div>
                    <div style={{ fontSize: 12, color: "#888", marginBottom: 8 }}>Last Turn Tokens</div>
                    <div style={{ fontSize: 12, display: "flex", flexDirection: "column", gap: 4 }}>
                        <div>Prompt: <span style={{ color: "#c9a84c" }}>{tokenUsage.prompt_tokens}</span></div>
                        <div>Response: <span style={{ color: "#c9a84c" }}>{tokenUsage.response_tokens}</span></div>
                        <div>Total: <span style={{ color: "#c9a84c" }}>{tokenUsage.total_tokens}</span></div>
                    </div>
                </div>
            )}
        </div>
    )
}