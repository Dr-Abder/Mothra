import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
              L'IA au service de la peau
            </h1>
            <p className="text-xl md:text-2xl text-gray-700">
              Mothra : Deep Learning pour le diagnostic dermatologique
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                to="/diagnostic"
                className="px-8 py-4 bg-black text-white rounded-lg text-center font-semibold hover:bg-gray-800 transition-colors"
              >
                Effectuez un diagnostic
              </Link>
              <a
                href="#mothra-v2"
                className="px-8 py-4 bg-gray-light text-black rounded-lg text-center font-semibold hover:bg-gray-300 transition-colors"
              >
                Mothra-V.2
              </a>
            </div>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="aspect-square rounded-2xl bg-gray-200 overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=800&h=800&fit=crop"
                alt="Médecin avec stéthoscope"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Future Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="space-y-12">
          <div>
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              L'avenir du diagnostic médical
            </h2>
            <p className="text-lg text-gray-700 max-w-3xl leading-relaxed">
              Mothra utilise des modèles de Deep Learning de pointe pour analyser
              les images dermatologiques avec une précision exceptionnelle. Notre
              technologie combine l'expertise médicale et l'intelligence
              artificielle pour offrir des diagnostics rapides et fiables.
            </p>
          </div>

          {/* Features List */}
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
              <p className="text-lg">
                Analyse instantanée de vos images dermatologiques
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
              <p className="text-lg">
                Résultats fiables basés sur des millions d'images analysées
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
              <p className="text-lg">
                Recommandations personnalisées pour chaque diagnostic
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
              <p className="text-lg">
                Confidentialité et sécurité garanties (conformité RGPD)
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Three Cards Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Card 1 - Scientifique */}
          <div className="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
            <div className="aspect-video bg-gray-200">
              <img
                src="https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=600&h=400&fit=crop"
                alt="Structure moléculaire"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="p-6 space-y-4">
              <h3 className="text-2xl font-bold">Scientifique</h3>
              <p className="text-gray-700 leading-relaxed">
                Notre modèle est entraîné sur des datasets médicaux validés par
                des dermatologues experts. Nous utilisons des architectures CNN
                de dernière génération pour garantir la précision des diagnostics.
              </p>
            </div>
          </div>

          {/* Card 2 - Utilisateur */}
          <div className="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
            <div className="aspect-video bg-gray-200">
              <img
                src="https://images.unsplash.com/photo-1576086213369-97a306d36557?w=600&h=400&fit=crop"
                alt="Cellule rose"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="p-6 space-y-4">
              <h3 className="text-2xl font-bold">Utilisateur</h3>
              <p className="text-gray-700 leading-relaxed">
                Une interface simple et intuitive pour uploader vos images.
                Recevez des résultats détaillés en quelques secondes et
                consultez l'historique complet de vos analyses à tout moment.
              </p>
            </div>
          </div>

          {/* Card 3 - Visionnaire */}
          <div className="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
            <div className="aspect-video bg-gray-200">
              <img
                src="https://images.unsplash.com/photo-1530497610245-94d3c16cda28?w=600&h=400&fit=crop"
                alt="Scanner médical"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="p-6 space-y-4">
              <h3 className="text-2xl font-bold">Visionnaire</h3>
              <p className="text-gray-700 leading-relaxed">
                Mothra représente l'avenir de la dermatologie. Notre vision est
                de rendre le diagnostic précoce accessible à tous, partout dans
                le monde, grâce à l'intelligence artificielle.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
