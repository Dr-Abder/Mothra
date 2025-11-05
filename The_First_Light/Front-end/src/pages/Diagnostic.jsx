import { useState } from 'react';

const Diagnostic = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    // Simulation d'analyse (remplacer par appel API réel)
    setTimeout(() => {
      setResult({
        diagnostic: "L'image analysée est probablement bénigne",
        confidence: 92,
        recommendation:
          "Aucune action immédiate requise. Surveillance recommandée. Consultez un dermatologue en cas de changement d'aspect, de taille ou de couleur.",
        details:
          "Le modèle Mothra CNN v1 a analysé votre image et détecté une lésion cutanée avec des caractéristiques bénignes. La symétrie, les bords et la couleur sont dans les normes.",
      });
      setIsAnalyzing(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        {/* Header */}
        <div className="mb-12 max-w-3xl">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Lancez un diagnostic
          </h1>
          <p className="text-lg text-gray-700 leading-relaxed">
            Les examens sont réalisés avec la dernière version de notre modèle
            d'IA Mothra CNN. Uploadez une image claire de la zone cutanée à
            analyser. Notre algorithme vous fournira un diagnostic détaillé avec
            un niveau de confiance en quelques secondes.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Left - Upload Section */}
          <div className="space-y-6">
            {/* Upload Zone */}
            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className="relative border-4 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:border-black transition-colors cursor-pointer bg-white"
            >
              {preview ? (
                <div className="relative">
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-h-96 mx-auto rounded-lg"
                  />
                  <button
                    onClick={() => {
                      setPreview(null);
                      setSelectedFile(null);
                      setResult(null);
                    }}
                    className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600"
                  >
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="w-20 h-20 mx-auto bg-gray-200 rounded-full flex items-center justify-center">
                    <svg
                      className="w-10 h-10 text-gray-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                  </div>
                  <div>
                    <p className="text-lg font-semibold mb-2">
                      Glissez votre image ici
                    </p>
                    <p className="text-gray-600">
                      ou cliquez pour sélectionner un fichier
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      Formats acceptés : JPG, PNG, WEBP (max 10MB)
                    </p>
                  </div>
                </div>
              )}
              <input
                type="file"
                onChange={handleFileChange}
                accept="image/jpeg,image/png,image/webp"
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={handleAnalyze}
                disabled={!selectedFile || isAnalyzing}
                className={`flex-1 px-8 py-4 rounded-lg font-semibold transition-colors ${
                  selectedFile && !isAnalyzing
                    ? 'bg-black text-white hover:bg-gray-800'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {isAnalyzing ? (
                  <span className="flex items-center justify-center">
                    <svg
                      className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    Analyse en cours...
                  </span>
                ) : (
                  "Commencez l'examen"
                )}
              </button>
              <label className="flex-1 px-8 py-4 bg-gray-light rounded-lg font-semibold text-center cursor-pointer hover:bg-gray-300 transition-colors">
                Upload un fichier
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept="image/jpeg,image/png,image/webp"
                  className="hidden"
                />
              </label>
            </div>

            {/* Info Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
              <h3 className="font-semibold mb-2 flex items-center">
                <svg
                  className="w-5 h-5 mr-2 text-blue-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
                Conseils pour une analyse optimale
              </h3>
              <ul className="space-y-1 text-sm text-gray-700">
                <li>• Prenez la photo en lumière naturelle</li>
                <li>• Assurez-vous que l'image est nette et bien cadrée</li>
                <li>• La zone à analyser doit être clairement visible</li>
                <li>• Évitez les ombres et les reflets</li>
              </ul>
            </div>
          </div>

          {/* Right - Results Section */}
          <div>
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <h2 className="text-3xl font-bold mb-6">Résultat du diagnostic</h2>

              {!result && !isAnalyzing && (
                <div className="text-center py-12 text-gray-500">
                  <svg
                    className="w-20 h-20 mx-auto mb-4 text-gray-300"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <p>Uploadez une image pour obtenir un diagnostic</p>
                </div>
              )}

              {isAnalyzing && (
                <div className="text-center py-12">
                  <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-black mb-4"></div>
                  <p className="text-lg">Analyse en cours...</p>
                  <p className="text-gray-600 mt-2">
                    Notre IA analyse votre image
                  </p>
                </div>
              )}

              {result && (
                <div className="space-y-6">
                  {/* Diagnostic */}
                  <div>
                    <h3 className="font-semibold text-lg mb-2">Diagnostic</h3>
                    <p className="text-gray-700 text-lg">{result.diagnostic}</p>
                  </div>

                  {/* Confidence */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="font-semibold">Niveau de confiance</span>
                      <span className="font-bold text-lg">
                        {result.confidence}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div
                        className="bg-green-500 h-4 rounded-full transition-all duration-1000"
                        style={{ width: `${result.confidence}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Details */}
                  <div>
                    <h3 className="font-semibold text-lg mb-2">
                      Détails de l'analyse
                    </h3>
                    <p className="text-gray-700 leading-relaxed">
                      {result.details}
                    </p>
                  </div>

                  {/* Recommendation */}
                  <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
                    <h3 className="font-semibold text-lg mb-2 flex items-center">
                      <svg
                        className="w-5 h-5 mr-2 text-yellow-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                      Recommandation
                    </h3>
                    <p className="text-gray-700 leading-relaxed">
                      {result.recommendation}
                    </p>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-4 pt-4">
                    <button className="flex-1 px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors">
                      Sauvegarder
                    </button>
                    <button className="flex-1 px-6 py-3 bg-gray-light rounded-lg hover:bg-gray-300 transition-colors">
                      Exporter PDF
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Diagnostic;
