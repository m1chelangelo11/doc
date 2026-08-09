function MessageHistory({ messageHistory }) {
  return (
    <div>
      {messageHistory.map((message, index) => (
        <p key={index}> {message} </p>
      ))}
    </div>
  );
}

export default MessageHistory;
