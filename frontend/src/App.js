


import React from "react";
import Chatbot from "./Chatbot";
import "./App.css"; // Global styles
import vuicodeLogo from "./vuicodebanner.png"; // Import the logo


function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <img src={vuicodeLogo} alt="VuiCode" className="logo" />
          <h1>My AI Assistant</h1>
        </div>
      </header>
      <main>
        <Chatbot />
      </main>
    </div>
  );
}

export default App;
