import React from "react";

export default function LoadingSpinner({ message = "Chargement..." }) {
  return (
    <div className="flex flex-col items-center justify-center mt-8">
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600"></div>
      <p className="mt-4 text-blue-600 font-semibold">{message}</p>
    </div>
  );
}
