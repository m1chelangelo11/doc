import "./App.css";
import useFileUpload from "./hooks/useFileUpload";
import useChat from "./hooks/useChat";
import SendButton from "./components/SendButton";
import MessageHistory from "./components/MessageHistory";
import FileInput from "./components/FileInput";
import AttachmentList from "./components/AttachmentList";

function App() {
  const fileUpload = useFileUpload();
  const chat = useChat(fileUpload);

  return (
    <>
      <MessageHistory messageHistory={chat.messageHistory} />
      <input
        value={chat.userInput}
        onChange={(e) => chat.setUserInput(e.target.value)}
      />
      <SendButton onClick={chat.handleSend} />
      <label>
        <input type="checkbox"
          checked = {fileUpload.useRag}
          onChange={(e) => fileUpload.setUseRag(e.target.checked)}
        />
      Use RAG?
      </label>
      <FileInput
        inputRef={fileUpload.fileInput}
        onChange={fileUpload.handleUpload}
      />
      <AttachmentList
        documents={fileUpload.documents}
        removeDocument={fileUpload.removeDocument}
        images={fileUpload.images}
        removeImage={fileUpload.removeImage}
      />
      {fileUpload.error && <p>{fileUpload.error}</p>}
    </>
  );
}

export default App;
