import { useState } from "react";
import api from "../services/api";

function ChatPage() {

  const [userId, setUserId] =
    useState("demo-user");

  const [message, setMessage] =
    useState("");

  const [messages, setMessages] =
    useState([]);

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
      <h1>
        Persistent Sales Assistant
      </h1>

      <input
        value={userId}
        onChange={(e) =>
          setUserId(
            e.target.value
          )
        }
        placeholder="User ID"
      />

      <br />
      <br />

      <textarea
        rows={4}
        cols={80}
        value={message}
        onChange={(e) =>
          setMessage(
            e.target.value
          )
        }
      />

      <br />
      <br />

      <button
        onClick={sendMessage}
      >
        Send
      </button>

      <hr />

      {messages.map(
        (msg, idx) => (
          <div key={idx}>
            <h3>
              {msg.role}
            </h3>

            <p>
              {msg.content}
            </p>

            {msg.eval && (
              <>
                <h4>
                  Evaluation
                </h4>

                <pre>
                  {
                    JSON.stringify(
                      msg.eval,
                      null,
                      2
                    )
                  }
                </pre>
              </>
            )}

            <hr />
          </div>
        )
      )}
    </div>
  );
}

export default ChatPage;