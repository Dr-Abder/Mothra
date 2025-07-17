import React from "react";

export default function ImagePreview({ src, alt }) {
  return (
    <div className="mt-4">
      <img
        src={src}
        alt={alt}
        className="mx-auto max-w-full max-h-64 rounded-lg shadow-md object-contain"
      />
    </div>
  );
}
