const Dashboard = () => {
  // Mock data pour les diagnostics
  const diagnostics = [
    {
      id: 1,
      number: "001",
      date: "21/10/25",
      image: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400&h=300&fit=crop",
      result: "L'image analysée est probablement bénigne",
      confidence: 92,
      recommendation:
        "Aucune action immédiate requise. Surveillance recommandée. Consultez un dermatologue en cas de changement.",
    },
    {
      id: 2,
      number: "002",
      date: "18/10/25",
      image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400&h=300&fit=crop",
      result: "Peau normale détectée",
      confidence: 96,
      recommendation:
        "Résultat normal. Continuez votre routine de soins habituels et protégez votre peau du soleil.",
    },
    {
      id: 3,
      number: "003",
      date: "15/10/25",
      image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=300&fit=crop",
      result: "Zone suspecte détectée",
      confidence: 78,
      recommendation:
        "Consultation dermatologique recommandée dans les 2 semaines. Surveillez tout changement de couleur ou de taille.",
    },
  ];

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

        {/* Diagnostics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {diagnostics.map((diagnostic) => (
            <div
              key={diagnostic.id}
              className="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow"
            >
              {/* Image */}
              <div className="aspect-[4/3] bg-gray-200">
                <img
                  src={diagnostic.image}
                  alt={`Diagnostic ${diagnostic.number}`}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Content */}
              <div className="p-6 space-y-4">
                {/* Header */}
                <div>
                  <h3 className="text-lg font-semibold">
                    Diagnostic n°{diagnostic.number}
                  </h3>
                  <p className="text-sm text-gray-600">{diagnostic.date}</p>
                </div>

                {/* Result */}
                <div className="space-y-2">
                  <p className="text-gray-700">
                    {diagnostic.result}{" "}
                    <span className="font-semibold">
                      (confiance : {diagnostic.confidence} %)
                    </span>
                  </p>

                  {/* Confidence Bar */}
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        diagnostic.confidence >= 90
                          ? "bg-green-500"
                          : diagnostic.confidence >= 70
                          ? "bg-yellow-500"
                          : "bg-orange-500"
                      }`}
                      style={{ width: `${diagnostic.confidence}%` }}
                    ></div>
                  </div>
                </div>

                {/* Recommendation */}
                <div className="pt-2 border-t border-gray-200">
                  <p className="text-sm font-semibold mb-1">Recommandation :</p>
                  <p className="text-sm text-gray-700 leading-relaxed">
                    {diagnostic.recommendation}
                  </p>
                </div>

                {/* Actions */}
                <div className="flex gap-2 pt-2">
                  <button className="flex-1 px-4 py-2 bg-black text-white rounded-lg text-sm hover:bg-gray-800 transition-colors">
                    Voir détails
                  </button>
                  <button className="px-4 py-2 bg-gray-light rounded-lg text-sm hover:bg-gray-300 transition-colors">
                    Exporter
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State (si pas de diagnostics) */}
        {diagnostics.length === 0 && (
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
            <a
              href="/diagnostic"
              className="inline-block px-8 py-4 bg-black text-white rounded-lg font-semibold hover:bg-gray-800 transition-colors"
            >
              Effectuez un diagnostic
            </a>
          </div>
        )}

        {/* Stats Section */}
        <section className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <h3 className="text-4xl font-bold mb-2">{diagnostics.length}</h3>
            <p className="text-gray-700">Analyses effectuées</p>
          </div>
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <h3 className="text-4xl font-bold mb-2">
              {Math.round(
                diagnostics.reduce((acc, d) => acc + d.confidence, 0) /
                  diagnostics.length
              )}
              %
            </h3>
            <p className="text-gray-700">Confiance moyenne</p>
          </div>
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <h3 className="text-4xl font-bold mb-2">
              {diagnostics[0]?.date || "N/A"}
            </h3>
            <p className="text-gray-700">Dernière analyse</p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
