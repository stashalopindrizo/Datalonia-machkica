import React from "react";
import type { Message } from "../../types";

type Props = {
  messages: Message[];
  endRef: React.RefObject<HTMLDivElement>; 
  containerRef: React.RefObject<HTMLDivElement>;
};

export default function MessageList({ messages, endRef, containerRef }: Props) {
  return (
    <div className="messages" ref={containerRef}>
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`msg ${msg.role === "user" ? "user" : "ai"}`}
        >
          <div>
            {msg.content}
            <small className="time">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </small>
          </div>
        </div>
      ))}
      <div ref={endRef} />
    </div>
  );
}
