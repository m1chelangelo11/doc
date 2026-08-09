import "./App.css";
import useFileUpload from "./hooks/useFileUpload";
import useChat from "./hooks/useChat";
import SendButton from "./components/SendButton";
import MessageHistory from "./components/MessageHistory";
import FileInput from "./components/FileInput";

function App() {
  const fileUpload = useFileUpload();
  const chat = useChat(fileUpload);

  return (
    <>
      <input
        value={chat.userInput}
        onChange={(e) => chat.setUserInput(e.target.value)}
      />
      <SendButton onClick={chat.handleSend} />
      <MessageHistory messageHistory={chat.messageHistory} />
      <FileInput
        inputRef={fileUpload.fileInput}
        onChange={fileUpload.handleUpload}
      />
    </>
  );
}

export default App;
