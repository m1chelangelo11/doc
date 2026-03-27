import './App.css'
import {useState} from 'react'

function App() {
  const [userInput, setUserInput] = useState("")
  const [messageHistory, updateMessageHistory] = useState([])

  async function handleSend() {
    updateMessageHistory([...messageHistory, userInput])
    setUserInput("")

    const response = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json"},
      body: JSON.stringify({ content: userInput})
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
        Send Message
      </button>

    </div>

  )
}

export default App
