import React, { useState, useEffect } from "react";
import "./ConversationHistorySidebar.css";

const ConversationHistorySidebar = ({ result }) => {
  const [conversationHistory, setConversationHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchConversationHistory = async () => {
    try {
      const response = await fetch(" http://127.0.0.1:8000/chat-history");
      if (!response.ok) {
        throw new Error("Failed to fetch conversation history");
      }
      const data = await response.json();
      setConversationHistory(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConversationHistory();
  }, [result]);

  return (
    <div className="sidebar-history">
      <h2>Conversation History</h2>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <ul className="conversation-list">
          {conversationHistory.map((conversation, index) => (
            <li key={index} className="conversation-item">
              <div className="user-query">
                <strong>User Query:</strong> {conversation.user_query}
              </div>
              <div className="sql-query">
                <strong>SQL Query:</strong> {conversation.sql_query}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ConversationHistorySidebar;
