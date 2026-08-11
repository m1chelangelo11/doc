import { useState } from "react";

export default function useChat(fileUpload) {
  const [userInput, setUserInput] = useState("");
  const [messageHistory, updateMessageHistory] = useState([]);

  async function handleSend() {
    updateMessageHistory((prev) => [...prev, userInput]);

    const content = [{ type: "text", text: userInput }];

    for (const image of fileUpload.images) {
      content.push({
        type: "file",
        file: {
          filename: image.filename,
          file_data: image.data,
        },
      });
    }

    setUserInput("");

    const response = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content, use_rag: fileUpload.useRag }),
    });

    const data = await response.json();
    console.log(data);
    updateMessageHistory((prev) => [...prev, data]);
  }

  return { userInput, setUserInput, messageHistory, handleSend };
}