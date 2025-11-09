import { useState, useEffect } from 'react';
import { analyses as analysesAPI, images as imagesAPI } from '../services/api';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadAnalyses();
  }, []);

  const loadAnalyses = async () => {
    try {
      setLoading(true);
      const data = await analysesAPI.getAll();
      setAnalyses(data);
      setError('');
    } catch (err) {
      console.error('Erreur lors du chargement des analyses:', err);
      setError('Impossible de charger vos analyses');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette analyse?')) {
      return;
    }

    try {
      await analysesAPI.delete(id);
      // Recharger la liste
      loadAnalyses();
    } catch (err) {
      console.error('Erreur lors de la suppression:', err);
      alert('Erreur lors de la suppression de l\'analyse');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit',
    });
  };

  const getImageUrl = (analyseId) => {
    return imagesAPI.getAnalysisImage(analyseId);
  };

  const calculateStats = () => {
    if (analyses.length === 0) return { avgConfidence: 0, lastDate: 'N/A' };

    const avgConfidence = Math.round(
      analyses.reduce((acc, a) => acc + (a.confidence * 100), 0) / analyses.length
    );

    const lastDate = formatDate(analyses[0].created_at);

    return { avgConfidence, lastDate };
  };

  const stats = calculateStats();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-black mb-4"></div>
          <p className="text-lg">Chargement de vos analyses...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Gardez un œil sur vos analyses
          </h1>
          <p className="text-xl text-gray-700">
            Retrouvez tous vos diagnostics
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-8">
            {error}
          </div>
        )}

        {/* Empty State */}
        {analyses.length === 0 ? (
          <div className="text-center py-20">
            <div className="mb-6">
              <svg
                className="w-24 h-24 mx-auto text-gray-400"
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
            </div>
            <h3 className="text-2xl font-semibold mb-2">
              Aucun diagnostic pour le moment
            </h3>
            <p className="text-gray-600 mb-6">
              Effectuez votre premier diagnostic pour commencer
            </p>
            <Link
              to="/diagnostic"
              className="inline-block px-8 py-4 bg-black text-white rounded-lg font-semibold hover:bg-gray-800 transition-colors"
            >
              Effectuez un diagnostic
            </Link>
          </div>
        ) : (
          <>
            {/* Diagnostics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
              {analyses.map((analyse, index) => (
                <div
                  key={analyse.id}
                  className="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow"
                >
                  {/* Image */}
                  <div className="aspect-[4/3] bg-gray-200 relative">
                    <img
                      src={getImageUrl(analyse.id)}
                      alt={`Diagnostic ${index + 1}`}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.src = 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400&h=300&fit=crop';
                      }}
                    />
                  </div>

                  {/* Content */}
                  <div className="p-6 space-y-4">
                    {/* Header */}
                    <div>
                      <h3 className="text-lg font-semibold">
                        Diagnostic n°{String(index + 1).padStart(3, '0')}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {formatDate(analyse.created_at)}
                      </p>
                    </div>

                    {/* Result */}
                    <div className="space-y-2">
                      <p className="text-gray-700">
                        {analyse.diagnostic}
                      </p>
                      <p className="font-semibold">
                        Confiance : {(analyse.confidence * 100).toFixed(1)}%
                      </p>

                      {/* Confidence Bar */}
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            analyse.confidence >= 0.9
                              ? 'bg-green-500'
                              : analyse.confidence >= 0.7
                              ? 'bg-yellow-500'
                              : 'bg-orange-500'
                          }`}
                          style={{ width: `${analyse.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                      <button
                        onClick={() => handleDelete(analyse.id)}
                        className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg text-sm hover:bg-red-600 transition-colors"
                      >
                        Supprimer
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Stats Section */}
            <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <h3 className="text-4xl font-bold mb-2">{analyses.length}</h3>
                <p className="text-gray-700">Analyses effectuées</p>
              </div>
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <h3 className="text-4xl font-bold mb-2">
                  {stats.avgConfidence}%
                </h3>
                <p className="text-gray-700">Confiance moyenne</p>
              </div>
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <h3 className="text-4xl font-bold mb-2">{stats.lastDate}</h3>
                <p className="text-gray-700">Dernière analyse</p>
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
