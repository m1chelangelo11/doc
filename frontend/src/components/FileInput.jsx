import { Paperclip } from "lucide-react";

function FileInput({ inputRef, onChange }) {
  return (
    <div>
      <input
        type="file"
        ref={inputRef}
        onChange={onChange}
        multiple
        className="hidden"
      />
      <button
        onClick={() => inputRef.current.click()}
        className="text-ink/50 hover:text-accent transition-colors p-2"
      >
        <Paperclip size={18} />
      </button>
    </div>
  );
}

export default FileInput;
