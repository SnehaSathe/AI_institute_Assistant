import { useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userMessage,
          }),
        }
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">

      <div className="chat-container">

        <header className="header">
          <div>
            <h1>AI Institute Assistant</h1>
            <p>Ask me anything about our institute</p>
          </div>

          <button onClick={clearChat}>
            Clear
          </button>
        </header>

        <main className="messages">

          {messages.length === 0 && (
            <div className="welcome">
              <h2>👋 Hello!</h2>

              <p>
                I'm your AI Institute Assistant.
              </p>

              <div className="suggestions">

                <button
                  onClick={() =>
                    setInput("What courses do you offer?")
                  }
                >
                  What courses do you offer?
                </button>

                <button
                  onClick={() =>
                    setInput("What are the class timings?")
                  }
                >
                  What are the class timings?
                </button>

                <button
                  onClick={() =>
                    setInput("How can I contact the institute?")
                  }
                >
                  Contact information
                </button>

              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role}`}
            >
              <div className="avatar">
                {message.role === "user" ? "👤" : "🤖"}
              </div>

              <div className="bubble">
                {message.role === "assistant" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  message.content
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="avatar">🤖</div>

              <div className="bubble">
                Thinking...
              </div>
            </div>
          )}

        </main>

        <div className="input-area">

          <input
            type="text"
            placeholder="Ask something..."
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={handleKeyDown}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

export default App;