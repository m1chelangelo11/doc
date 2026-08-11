function FileInput({ inputRef, onChange }) {
  return <input type="file" ref={inputRef} onChange={onChange} multiple/>;
}

export default FileInput;
