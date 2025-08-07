import React, { useState } from "react";
import { fetchData } from "../services/api";
import QueryDisplay from "./QueryDisplay";

// Importing Font Awesmome React Component
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"; // Importing FontAwesomeIcon component

// Importing FontAwesome Globally
import { library } from "@fortawesome/fontawesome-svg-core"; // Importing library for FontAwesome icons

// import your icons
import { fab } from "@fortawesome/free-brands-svg-icons"; // Importing FontAwesome brands icons
import { fas } from "@fortawesome/free-solid-svg-icons"; // Importing FontAwesome solid icons
import { far } from "@fortawesome/free-regular-svg-icons"; // Importing FontAwesome regular icons
library.add(fab, fas, far); // Adding imported icons to the library

const Chatbot = ({ result, setResult }) => {
  const [input, setInput] = useState("");
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setIsLoading(true);
      const data = await fetchData(input);
      console.log("Generated Query:", data.SQLQuery);
      setQuery(() => data.SQLQuery);
      const queryResult = data.FetchedData;
      console.log(data);
      setError(null);
      console.log("Query Result:", queryResult);
      setResult(() => queryResult);
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Function component for rendering loader
  function Loader({ faicon = "fa-solid fa-spinner", toSpin = true }) {
    return (
      <p className="loader">
        {" "}
        <span>
          <FontAwesomeIcon icon={faicon} spin={toSpin} />
        </span>
        Loading...
      </p>
    );
  }
  const inactiveStyle = {
    opacity: 0.3,
    cursor: "not-allowed",
  };

  const activeStyle = {
    opacity: 1,
  };

  return (
    <div className="chatbot-container">
      <h1>Text to SQL Chatbot</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
        />
        <button
          type="submit"
          disabled={input === ""}
          style={input === "" ? inactiveStyle : activeStyle}
        >
          Submit
        </button>
      </form>

      {/* Use QueryDisplay component here */}
      {isLoading ? (
        <Loader faicon="fa-solid fa-spinner" toSpin={true} />
      ) : error ? (
        <pre style={{ backgroundColor: "#f77777", opacity: 0.9 }}>
          <FontAwesomeIcon icon="fa-solid fa-warning" size="xl" />
          <h2 style={{ display: "inline", marginLeft: "10px" }}>
            Failed to fetch Data
          </h2>
          <code style={{ display: "block", marginTop: "10px" }}>{error}</code>
        </pre>
      ) : (
        <QueryDisplay query={query} result={result} />
      )}
    </div>
  );
};

export default Chatbot;
