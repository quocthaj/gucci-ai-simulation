import { useState } from "react"
import ChatWindow from "./assets/components/ChatWindow"
import StatePanel from "./assets/components/StatePanel"

export default function App() {
  const [state, setState] = useState({
    stagnation_counter: 0,
    rapport_score: 0.5,
    competencies_covered: [],
    injection_fired: false
  })
  const [tokenUsage, setTokenUsage] = useState(null)

  return (
    <div style={{
      display: "flex",
      height: "100vh",
      fontFamily: "sans-serif",
      background: "#f5f0eb"
    }}>
      {/* Chat chiếm 70% */}
      <div style={{ flex: 7, display: "flex", flexDirection: "column" }}>
        <header style={{
          padding: "16px 24px",
          background: "#1a1a1a",
          color: "#c9a84c",
          fontWeight: "bold",
          fontSize: 18
        }}>
          Gucci Group — CHRO Simulation
        </header>
        <ChatWindow
          onStateUpdate={setState}
          onTokenUpdate={setTokenUsage}
        />
      </div>

      {/* State panel chiếm 30% */}
      <StatePanel state={state} tokenUsage={tokenUsage} />
    </div>
  )
}