import { useState } from "react";

export default function useChat(fileUpload) {
  const [userInput, setUserInput] = useState("");
  const [messageHistory, updateMessageHistory] = useState([]);

  async function handleSend() {
    updateMessageHistory((prev) => [...prev, userInput]);

    const content = [{ type: "text", text: userInput }];

    if (fileUpload.fileData) {
      if (fileUpload.contentType === "base64") {
        content.push({
          type: "file",
          file: {
            filename: fileUpload.fileName,
            file_data: fileUpload.fileData,
          },
        });
      } else if (fileUpload.contentType === "text") {
        content.push({
          type: "text",
          text: `\n\n --- ${fileUpload.fileName} content --- \n ${fileUpload.fileData} \n ---------------------------- \n`,
        });
      }
    }

    setUserInput("");
    fileUpload.updateFileData(null);
    fileUpload.updateContentType(null);

    const response = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });

    const data = await response.json();
    console.log(data);
    updateMessageHistory((prev) => [...prev, data]);
  }

  return { userInput, setUserInput, messageHistory, handleSend };
}
