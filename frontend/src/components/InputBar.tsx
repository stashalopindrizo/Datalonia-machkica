import React from "react";
import { Send } from "lucide-react";

type Props = {
  input: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSend: () => void;
  onKeyPress: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
};

export default function InputBar({
  input,
  loading,
  onChange,
  onSend,
  onKeyPress,
}: Props) {
 return (
  <div className="inputRow">
    <textarea
      placeholder="Napiši poruku Medi..."
      value={input}
      onChange={(e) => onChange(e.target.value)}
      onKeyDown={onKeyPress}
      disabled={loading}
    />
    <button
      onClick={onSend}
      className="p-2 bg-blue-700 rounded-md hover:bg-blue-600"
      disabled={loading}
    >
      <Send className="w-5 h-5" />
    </button>
  </div>
);
}


