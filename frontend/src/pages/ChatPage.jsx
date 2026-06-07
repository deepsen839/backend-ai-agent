import { useEffect, useRef, useState } from "react";
import api from "../services/api";

function ChatPage() {
  const [userId, setUserId] =
    useState("demo-user");

  const [message, setMessage] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const bottomRef = useRef(null);

  useEffect(() => {
    loadHistory();
  }, [userId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages]);

  const loadHistory = async () => {
    try {
      const response =
        await api.get(
          `/chat/${userId}/history`
        );

      const sortedMessages =
        response.data.sort(
          (a, b) =>
            new Date(a.created_at) -
            new Date(b.created_at)
        );

      setMessages(sortedMessages);

    } catch (err) {
      console.error(err);
    }
  };

  const sendMessage = async () => {

    if (!message.trim()) {
      return;
    }

    try {

      const response =
        await api.post(
          `/chat/${userId}`,
          {
            message
          }
        );

      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: message
        },
        {
          role: "assistant",
          content:
            response.data.response,
          eval:
            response.data.eval
        }
      ]);

      setMessage("");

    } catch (err) {

      console.error(err);

    }
  };

return (
  <div
    style={{
      padding: "2rem",
      maxWidth: "1000px",
      margin: "0 auto"
    }}
  >
    <h1>Persistent Sales Assistant</h1>

    <input
      value={userId}
      onChange={(e) =>
        setUserId(e.target.value)
      }
      placeholder="User ID"
    />

    <br />
    <br />

    {/* Chat History */}
    <div
      style={{
        height: "500px",
        overflowY: "auto",
        border: "1px solid #ccc",
        padding: "10px",
        marginBottom: "20px"
      }}
    >
      {messages.map((msg, idx) => (
        <div key={idx}>
          <h3>{msg.role}</h3>

          <p>{msg.content}</p>

          {msg.eval && (
            <>
              <h4>Evaluation</h4>

              <pre>
                {JSON.stringify(
                  msg.eval,
                  null,
                  2
                )}
              </pre>
            </>
          )}

          <hr />
        </div>
      ))}

      <div ref={bottomRef}></div>
    </div>

    {/* Input Area */}
    <textarea
      rows={4}
      cols={80}
      value={message}
      onChange={(e) =>
        setMessage(e.target.value)
      }
      placeholder="Type your message..."
    />

    <br />
    <br />

    <button onClick={sendMessage}>
      Send
    </button>
  </div>
);
}

export default ChatPage;