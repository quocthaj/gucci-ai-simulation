import { useState, useRef, useEffect } from "react"
import MessageBubble from "./MessageBubble"

const SESSION_ID = "demo_" + Date.now()

export default function ChatWindow({ onStateUpdate, onTokenUpdate }) {
    const [messages, setMessages] = useState([
        {
            role: "assistant",
            content: "Chào bạn. Tôi là CHRO của Gucci Group. Chúng ta bắt đầu nhé?"
        }
    ])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages])

    async function sendMessage() {
        if (!input.trim() || loading) return

        const userMsg = { role: "user", content: input }
        setMessages(prev => [...prev, userMsg])
        setInput("")
        setLoading(true)

        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: SESSION_ID,
                    persona_id: "chro",
                    user_message: input
                })
            })
            const data = await res.json()

            setMessages(prev => {
                const updated = [...prev]
                // Gắn flag vào message user vừa gửi (cuối mảng trước khi add assistant)
                if (data.safety_flags?.length > 0) {
                    updated[updated.length - 1] = {
                        ...updated[updated.length - 1],
                        flags: data.safety_flags
                    }
                }
                return [...updated, {
                    role: "assistant",
                    content: data.message
                }]
            })
            onStateUpdate(data.state)
            onTokenUpdate(data.token_usage)

        } catch (err) {
            setMessages(prev => [...prev, {
                role: "assistant",
                content: "⚠️ Lỗi kết nối server."
            }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
            {/* Messages */}
            <div style={{ flex: 1, overflowY: "auto", padding: 24, display: "flex", flexDirection: "column", gap: 12 }}>
                {messages.map((m, i) => <MessageBubble key={i} message={m} />)}
                {loading && <MessageBubble message={{ role: "assistant", content: "..." }} />}
                <div ref={bottomRef} />
            </div>

            {/* Input */}
            <div style={{ padding: 16, borderTop: "1px solid #ddd", display: "flex", gap: 8, background: "#fff" }}>
                <input
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && sendMessage()}
                    placeholder="Nhập câu hỏi cho CHRO..."
                    style={{ flex: 1, padding: "10px 16px", borderRadius: 24, border: "1px solid #ccc", fontSize: 14 }}
                />
                <button
                    onClick={sendMessage}
                    disabled={loading}
                    style={{
                        padding: "10px 20px",
                        background: "#1a1a1a",
                        color: "#c9a84c",
                        border: "none",
                        borderRadius: 24,
                        cursor: "pointer",
                        fontWeight: "bold"
                    }}
                >
                    Gửi
                </button>
            </div>
        </div>
    )
}