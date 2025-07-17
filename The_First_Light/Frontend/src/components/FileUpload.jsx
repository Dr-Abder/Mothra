// src/components/FileUpload.js
import React from "react";
import { Upload } from "lucide-react"; // Icône élégante, simple et moderne

export default function FileUpload({ onFileSelect }) {
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center py-24">
      <label htmlFor="file-upload" className="cursor-pointer group">
        <div className="bg-black rounded-full p-6 flex items-center justify-center group-hover:opacity-80 transition">
          <Upload className="text-white w-12 h-12" />
        </div>
        <input
          id="file-upload"
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="hidden"
        />
        <p className="mt-4 text-lg font-semibold text-black group-hover:underline transition">
          upload file
        </p>
      </label>
    </div>
  );
}
