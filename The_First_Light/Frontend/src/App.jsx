import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ImagePreview from './components/ImagePreview';
import LoadingSpinner from './components/LoadingSpinner';
import PredictionResult from './components/PredictionResult';

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (file) => {
    setImage(file);
    setPrediction(null);
  };

  const handleAnalyze = async () => {
    if (!image) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Erreur lors de la prédiction.');

      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error('Erreur :', error);
      alert('Échec de la prédiction.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setPrediction(null);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md text-center space-y-6">
        <h1 className="text-3xl font-bold text-blue-800">Mothra 🦋</h1>

        {!image && (
          <FileUpload onFileSelect={handleFileChange} onAnalyze={handleAnalyze} />
        )}

        {image && <ImagePreview file={image} />}

        {loading && <LoadingSpinner message="En cours d’analyse..." />}

        {prediction && !loading && (
          <PredictionResult
            result={prediction.result}
            score={prediction.prediction_score}
          />
        )}

        {image && !loading && (
          <button
            onClick={handleAnalyze}
            className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
          >
            Lancer l’analyse
          </button>
        )}

        {prediction && (
          <button
            onClick={handleReset}
            className="mt-2 text-blue-500 underline hover:text-blue-700"
          >
            Refaire une analyse
          </button>
        )}
      </div>
    </div>
  );
}

export default App;
