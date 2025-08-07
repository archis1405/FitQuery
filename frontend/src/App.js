import React, { useState } from "react";
import Chatbot from "./components/Chatbot";
import Sidebar from "./components/Sidebar";
import History from "./components/History";

const App = () => {
  // Lift the result state to the App component
  const [result, setResult] = useState(null);

  return (
    <div className="app-container">
      <Sidebar />
      <Chatbot result={result} setResult={setResult} />
      <History result={result} />
    </div>
  );
};

export default App;
