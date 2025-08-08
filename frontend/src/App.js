


import React from "react";
import Chatbot from "./Chatbot";
import "./App.css"; // Global styles

console.log('Chatbot import:', Chatbot)

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>My AI Assistant</h1>
      </header>
      <main>
        <Chatbot />
      </main>
    </div>
  );
}

export default App;
