import { useState, useRef } from "react";

const readFile = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);

    reader.readAsDataURL(file);
  });
};

export default function useFileUpload() {
  const fileInput = useRef(null);
  const [fileData, updateFileData] = useState(null);
  const [fileName, updateFileName] = useState(null);
  const [contentType, updateContentType] = useState(null);

  async function handleUpload() {
    const file_data = fileInput.current.files[0];

    if (!file_data) {
      console.error("No file selected");
      return;
    }

    const isOfficeFile = file_data.type.includes(
      "application/vnd.openxmlformats-officedocument",
    );

    if (isOfficeFile) {
      const formData = new FormData();
      formData.append("file", file_data);

      const response = await fetch("http://localhost:8000/parse_file", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Backend error: ", errorData.detail || "Unknown error");
        return;
      }

      const data = await response.json();
      updateContentType("text");
      updateFileData(data.filedata);
      updateFileName(data.filename);
    } else {
      const base64Data = await readFile(file_data);
      updateContentType("base64");
      updateFileData(base64Data);
      updateFileName(file_data.name);
    }
  }
  return {
    fileName,
    fileData,
    fileInput,
    contentType,
    handleUpload,
    updateFileData,
    updateContentType,
  };
}
