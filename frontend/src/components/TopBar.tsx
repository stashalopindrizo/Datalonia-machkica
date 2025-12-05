import React from "react";

type Status = "connected" | "mock" | "offline";

type Props = {
  title: string;
  status: Status;
};

export default function TopBar({ title, status }: Props) {
  const dot =
    status === "connected" ? "bg-green-500" :
    status === "mock"       ? "bg-yellow-500" :
                              "bg-gray-400";

  const label =
    status === "connected" ? "connected" :
    status === "mock"       ? "mock" :
                              "offline";

  return (
    <header className="sticky top-0 z-10 mb-3 flex items-center justify-between border-b border-gray-200 bg-white/70 px-2 py-2 backdrop-blur">
      <h1 className="text-lg font-semibold tracking-wide">{title}</h1>
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <span className={`inline-block h-2.5 w-2.5 rounded-full ${dot}`} />
        <span className="uppercase tracking-wide">{label}</span>
      </div>
    </header>
  );
}

