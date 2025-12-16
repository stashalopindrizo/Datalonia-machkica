import React from "react";
import { Send } from "lucide-react";

type Props = {
  input: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSend: () => void;
  onKeyPress: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  onToggleBrain: () => void;
};

export default function InputBar({
  input,
  loading,
  onChange,
  onSend,
  onKeyPress, 
  onToggleBrain,
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
    
  {/* BRAIN dugme */}
  <button
    type="button"
    className="brainBtn" 
    onClick={() => {
     console.log("BRAIN CLICK");
     onToggleBrain?.();
    }}
    title="Brain"
    disabled={loading}
  >
    🧠
  </button> 

    <button
  type="button"
  onClick={onSend}
    className="p-2 bg-blue-700 rounded-md hover:opacity-90"
    disabled={loading}
    title="Send"
  >
    <Send className="w-5 h-5" />
  </button>
</div> 

);
}


