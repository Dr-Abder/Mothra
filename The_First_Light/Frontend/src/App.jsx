import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import ImagePreview from "./components/ImagePreview";
import LoadingSpinner from "./components/LoadingSpinner";
import PredictionResult from "./components/PredictionResult";

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState(null);

  const handleFileChange = (file) => {
    setImage(file);
    setImageUrl(URL.createObjectURL(file));
    setPrediction(null);
  };

  const handleAnalyze = async () => {
    if (!image) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", image);

    try {
      const start = Date.now();
      const response = await fetch("http://127.0.0.1:8000/predict/", {
        method: "POST",
        body: formData,
      });

      const elapsed = Date.now() - start;
      const delay = Math.max(3000 - elapsed, 0);

      if (!response.ok) throw new Error("Erreur lors de la prédiction.");
      const data = await response.json();

      setTimeout(() => {
        setPrediction(data);
        setLoading(false);
      }, delay);
    } catch (error) {
      console.error("Erreur :", error);
      alert("Échec de la prédiction.");
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setImageUrl(null);
    setPrediction(null);
  };

  return (
    <div className="min-h-screen bg-[#1a1a1a] text-white flex flex-col">
      {/* Header */}
      <header className="flex items-center p-4">
        <img src="/logo_mothra.png" alt="Mothra logo" className="h-10 w-auto" />
      </header>

      {/* Content */}
      <main className="flex-grow flex items-center justify-center px-4">
        <div className="bg-[#111] shadow-2xl rounded-2xl p-8 w-full max-w-3xl text-center space-y-6">
          <h1 className="text-4xl font-extrabold flex items-center justify-center gap-2">
            Mothra <span className="text-2xl">🦋</span>
          </h1>

          {!image && !prediction && (
            <>
              <FileUpload onFileSelect={handleFileChange} />
              {/* Bouton d’analyse personnalisé */}
              <button onClick={handleAnalyze}>
                <img src="/bouton-analyse.png" alt="Lancer analyse" className="mx-auto mt-4 w-40 hover:opacity-90 transition" />
              </button>
            </>
          )}

          {image && !prediction && <ImagePreview src={imageUrl} alt="Image sélectionnée" />}

          {loading && <LoadingSpinner message="Analyse en cours..." />}

          {!loading && prediction && (
            <PredictionResult
              result={prediction.result}
              score={prediction.prediction_score}
              imageSrc={imageUrl}
            />
          )}

          {/* Boutons après analyse */}
          {!loading && prediction && (
            <div className="flex flex-col gap-2 mt-4">
              <button
                onClick={handleAnalyze}
                className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
              >
                Relancer l’analyse
              </button>
              <button
                onClick={handleReset}
                className="text-blue-400 underline hover:text-blue-600"
              >
                Faire une nouvelle analyse
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
