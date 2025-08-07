// src/components/ExecutorTester.jsx
import React, { useState } from "react";

export default function ExecutorTester() {
  const [response, setResponse] = useState(null);

  const sendAction = async () => {
    const res = await fetch("http://localhost:8000/execute", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Origin": "http://localhost:3000", // pas toujours nécessaire, mais tu as eu des CORS stricts
      },
      body: JSON.stringify({
        actions: [{ type: "echo", message: "Hello depuis React 👋" }],
      }),
    });

    const data = await res.json();
    setResponse(data);
  };

  return (
    <div>
      <button onClick={sendAction}>Tester /execute</button>
      <pre>{response && JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}
