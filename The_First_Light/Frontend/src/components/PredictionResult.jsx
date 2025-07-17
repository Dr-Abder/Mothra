// src/components/PredictionResult.js
import React from "react";

export default function PredictionResult({ result, score, imageSrc, onReset }) {
  const isMalignant = result === "MALIN";

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="flex flex-col md:flex-row items-center md:items-start md:space-x-8 text-left max-w-3xl">
        {imageSrc && (
          <img
            src={imageSrc}
            alt="Image analysée"
            className="w-64 h-auto rounded-lg shadow-lg mb-6 md:mb-0"
          />
        )}
        <div className="text-gray-800 text-lg space-y-3">
          <p>
            <strong>Diagnostic de votre pathologie :</strong><br />
            D’après <strong>Mothra</strong>, votre pathologie est{" "}
            <span className={isMalignant ? "text-red-600 font-bold" : "text-green-600 font-bold"}>
              {isMalignant ? "maligne" : "inoffensive"}
            </span>.
          </p>
          <p>
            Score de confiance :{" "}
            <strong>{(score * 100).toFixed(2)}%</strong>
          </p>
          <p>
            Mais il est toujours recommandé de consulter l’avis d’une personne qualifiée.
          </p>
        </div>
      </div>

      <button
        onClick={onReset}
        className="mt-8 text-blue-600 hover:text-blue-800 underline text-base"
      >
        Refaire une analyse
      </button>
    </div>
  );
}
