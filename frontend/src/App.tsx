import React, { useEffect, useRef, useState } from "react";
import type { Message } from "../types";
import TopBar from "./components/TopBar";
import MessageList from "./components/MessageList";
import InputBar from "./components/InputBar";
import BrainPanel from "./components/BrainPanel";

const API_URL = "/api";

export default function App() {
  // --- state
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<"connected" | "offline">("offline"); 
  const [brainOpen, setBrainOpen] = useState(false); 
  const toggleBrain = () => setBrainOpen((v) => !v);
  
  const messagesEndRef = useRef<HTMLDivElement>(null); 
  const messagesContainerRef = useRef<HTMLDivElement>(null); 

  const [autoScroll, setAutoScroll]= useState(true); 

  useEffect(() => {
  const el = messagesContainerRef.current;
  if (!el) return;

  const onScroll = () => {
    const distanceFromBottom =
      el.scrollHeight - el.scrollTop - el.clientHeight;

    setAutoScroll(distanceFromBottom < 40);
  };

  el.addEventListener("scroll", onScroll);
  onScroll(); // inicijalno stanje

  return () => el.removeEventListener("scroll", onScroll);
}, []); 
   useEffect(() => {
  if (!brainOpen) return;

  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") setBrainOpen(false);
  };

  window.addEventListener("keydown", onKeyDown);
  return () => window.removeEventListener("keydown", onKeyDown);
}, [brainOpen]);

  // --- helpers
  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });



  // 2) ping status
  useEffect(() => {
    fetch(`${API_URL}/ping`)
      .then(r => setStatus(r.ok ? "connected" : "offline"))
      .catch(() => setStatus("offline"));
  }, []);

  // 3) auto scroll
  useEffect(() => {
  if (!autoScroll) return;
  scrollToBottom();
}, [messages, autoScroll]);

  // --- slanje poruke
  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const text = input.trim();
    setInput("");
    setLoading(true);

    // prikaži user poruku odmah
    setMessages(prev => [...prev, { role: "user", content: text, timestamp: new Date() } as Message]);

    try {
      // BE endpoint
      const res = await fetch(`${API_URL}/brain/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      // backend vraća { message: { role: 'assistant', content: '...' } }
      const replyText =
        data?.message?.content ??
        data?.reply ??
        data?.content ??
        "(prazan odgovor)";

      setMessages(prev => [...prev, { role: "assistant", content: replyText, timestamp: new Date() } as Message]);
    } catch (err) {
      console.error("sendMessage error:", err);
      setMessages(prev => [
        ...prev,
        { role: "system", content: "⚠️ Greška: chat nije uspeo. Pokušaj ponovo.", timestamp: new Date() } as Message,
      ]);
    } finally {
      setLoading(false);
      setTimeout(scrollToBottom, 0);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

// --- UI
return (
  <div className="halo-container">
    <div
      className="main-container"
      style={{ width: "100%", maxWidth: "1200px", margin: "0 auto" }}
    >
      <TopBar title="Datalonija" status={status} />

      <div className="text-white p-4">
        <h1 className="text-2xl font-bold mb-4">
          Datalonia · local AI by Stasha Lopin Drizo
        </h1>
        <div className="status">Status: born ready</div>
      </div>
     {/* CHAT + BRAIN U JEDNOJ KOLONI */}
<div
  style={{
    display: "flex",
    flexDirection: "column",
    width: "100%",
    gap: "16px",
    paddingBottom: "16px",
  }}
>
  {/* GORE: CHAT (poruke + input) */}
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      gap: "8px",
    }}
  >
    <MessageList messages={messages} 
    endRef={messagesEndRef} 
    containerRef={messagesContainerRef} />

    <InputBar
      input={input}
      loading={loading}
      onChange={setInput}
      onSend={sendMessage}
      onKeyPress={handleKeyPress} 
      onToggleBrain={toggleBrain}  
    />
  </div>

  {/* DOLE: BRAIN PANEL */}
  {brainOpen && (
  <div className="brainOverlay" onClick={() => setBrainOpen(false)}>
    <div
      className="brainDrawer"
      onClick={(e) => e.stopPropagation()}
    >
      <BrainPanel />
    </div>
  </div>
)}
</div> 
  </div>
</div> 

);
}