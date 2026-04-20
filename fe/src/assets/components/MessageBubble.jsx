export default function MessageBubble({ message }) {
    const isUser = message.role === "user"
    return (
        <div style={{ display: "flex", justifyContent: isUser ? "flex-end" : "flex-start" }}>
            <div style={{
                maxWidth: "70%",
                padding: "10px 16px",
                borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                background: isUser ? "#1a1a1a" : "#fff",
                color: isUser ? "#c9a84c" : "#333",
                fontSize: 14,
                lineHeight: 1.6,
                boxShadow: "0 1px 4px rgba(0,0,0,0.1)",
                whiteSpace: "pre-wrap",
                textAlign: "left"
            }}>
                {message.content}
                {message.flags?.length > 0 && (
                    <div style={{ marginTop: 6, fontSize: 11, color: "#e74c3c" }}>
                        ⚠️ {message.flags.join(", ")}
                    </div>
                )}
            </div>
        </div>
    )
}