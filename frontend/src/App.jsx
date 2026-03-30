import './App.css'
import {useState, useRef} from 'react'

function App() {
  const [userInput, setUserInput] = useState("")
  const [messageHistory, updateMessageHistory] = useState([])
  const fileInput = useRef(null)
  const [fileData, updateFileData] = useState(null)
  const [fileName, updateFileName] = useState(null)

  const readFile = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
    
      reader.onload = () => resolve(reader.result)
      reader.onerror = (error) => reject(error)
    
      reader.readAsDataURL(file)
    })
  }

  async function handleUpload() {
    const file_data = fileInput.current.files[0]

    if (!file_data) {
      console.error("No file selected") 
      return
    }

    const base64Data = await readFile(file_data);
    updateFileData(base64Data)
    updateFileName(file_data.name)
  }

  async function handleSend() {
    updateMessageHistory(prev => [...prev, userInput])

    const content = [
      {"type": "text", "text": userInput}
    ]

    if (fileData) {
      content.push({"type": "file", "file": {"filename": fileName, "file_data": fileData}})
    }
    
    setUserInput("")
    updateFileData(null)

    const response = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json"},
      body: JSON.stringify({content})
    }) 

    const data = await response.json()
    console.log(data)
    updateMessageHistory(prev => [...prev, data])
  }

  return (
    <div>
      <div>
        {messageHistory.map((message, index) => <p key = {index}> {message} </p>)}
      </div>

      <input 
        value = {userInput}
        onChange = {(e) => setUserInput(e.target.value)}
      />
      <button onClick = {handleSend}>
        Send
      </button>

      <input 
        type = "file"
        ref = {fileInput}
        onChange = {handleUpload}
      />

    </div>
  )
}

export default App
