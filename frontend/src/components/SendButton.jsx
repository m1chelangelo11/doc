import { ArrowUp } from "lucide-react";

function SendButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="bg-accent hover:bg-accent/90 text-paper rounded-md p-3 transition-colors"
    >
      <ArrowUp size={18} strokeWidth={2.5} />
    </button>
  );
}

export default SendButton;