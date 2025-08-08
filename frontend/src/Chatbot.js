


import React, { useState } from "react"; // React core + state hook
import axios from "axios";               // HTTP requests to backend
import "./Chatbot.css";                  // Import CSS styles for this component

function Chatbot() {
  const [messages, setMessages] = useState([]); // Store chat messages (user + bot)
  const [input, setInput] = useState("");       // Store text currently in the input box

  const sendMessage = async () => {
    const text = input.trim(); // Remove extra spaces
    if (!text) return;         // Stop if empty

    // User message object
    const userMsg = { id: Date.now(), role: "user", content: text };
    // Placeholder bot message (shows immediately under the user)
    const placeholder = { id: Date.now() + 1, role: "assistant", content: "…thinking" };
    // Position index of placeholder for later replacement
    const idx = messages.length + 1;

    // Add both messages to state
    setMessages(prev => [...prev, userMsg, placeholder]);
    // Clear input
    setInput("");

    try {
      // Send message to Flask backend
      const res = await axios.post("http://localhost:5000/chat", { message: text });
      const replyText = res.data.reply ?? "(no reply)";

      // Replace placeholder with real bot reply
      setMessages(prev => {
        const next = [...prev];
        next[idx] = { ...next[idx], content: replyText };
        return next;
      });
    } catch (err) {
      // Replace placeholder with error message
      setMessages(prev => {
        const next = [...prev];
        next[idx] = { ...next[idx], content: "⚠️ Error: " + (err.response?.data?.error || err.message) };
        return next;
      });
    }
  };

  // Send message on Enter key (without Shift)
  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chatbot-container"> {/* Outer container */}
      <h2 className="chatbot-title">🤖 GPT Chatbot</h2>

      {/* Scrollable chat message list */}
      <div className="chatbox">
        {messages.map((msg) => (
          <div key={msg.id} className="chat-message">
            <strong>{msg.role === "user" ? "You" : "Bot"}:</strong>{" "}
            <span className="chat-text">{msg.content}</span>
          </div>
        ))}
      </div>

      {/* Input area + Send button */}
      <div className="chat-input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)} // Update text as user types
          onKeyDown={onKeyDown}                      // Detect Enter key to send
          rows={2}
          className="chat-input"
          placeholder="Type your message and press Enter…"
        />
        <button onClick={sendMessage} className="chat-send-btn">
          Send
        </button>
      </div>
    </div>
  );
}

export default Chatbot; // Export component so App.js can use it
