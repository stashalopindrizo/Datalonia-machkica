import React from "react";

type Props = {
  children: React.ReactNode;
};

export default function BelaKucica({ children }: Props) {
  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-white to-gray-50 text-gray-900">
      <div className="mx-auto flex h-screen max-w-3xl flex-col px-4 sm:px-6 lg:px-8">
        {children}
      </div>
    </div>
  );
}

