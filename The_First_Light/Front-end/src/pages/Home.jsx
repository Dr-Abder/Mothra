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
                className="px-7 py-4 bg-black text-xl text-white rounded-xl text-center font-semibold"
              >
                Effectuez un diagnostic
              </Link>
              <a
                href="#mothra-v2"
                className="px-6 py-4 border-2 rounded-xl text-xl text-black text-center font-semibold"
                style={{borderColor: "#6c6b69"}}
              >
                Mothra-V.2
              </a>
            </div>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="aspect-square rounded-2xl bg-gray-200 overflow-hidden">
              <img
                src="/images/M2.jpg"
                alt="Médecin avec stéthoscope"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Future Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="space-y-4">
          <div>
            <h2 className="text-4xl md:text-5xl font-bold mb-6" >
              L'avenir du diagnostic médical
            </h2>
            {/* Sous-titre */}
            <h3 className="text-xl md:text-2xl font-medium mb-4 text-gray-600">
              Voir ce que l’œil ne voit pas
            </h3>
            <p className="text-lg max-w-3xl leading-relaxed" style={{ color: '#6c6b69' }}>
              La médecine évolue constamment grâce aux nouvelles technologies et à l’intelligence artificielle.<br />
              <br />Ces avancées permettent de :
            </p>
          </div>

          {/* Features List */}
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3" style={{backgroundColor: "#6c6b69"}}></div>
              <p className="text-lg"style={{ color: '#6c6b69' }}>
                Détecter plus tôt les maladies, avant que les symptômes ne deviennent visibles,
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3" style={{backgroundColor: "#6c6b69"}}></div>
              <p className="text-lg" style={{ color: '#6c6b69' }}>
                Améliorer la précision des diagnostics, pour des traitements plus efficaces,
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3" style={{backgroundColor: "#6c6b69"}}></div>
              <p className="text-lg" style={{ color: '#6c6b69' }}>
                Rendre les soins plus accessibles et personnalisés, en intégrant l’IA comme un allié du corps médical.
              </p>
            </div>
          </div>
          <h3 className="text-lg mb-4" style={{ color: '#6c6b69' }}>
            L’innovation technologique transforme ainsi la santé, en offrant des solutions plus rapides, fiables et intelligentes pour la prévention,
            le suivi et la prise en charge des patients.
          </h3>
        </div>
      </section>

      {/* Three Cards Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Card 1 - Scientifique */}
          <div className="rounded-2xl overflow-hidden">
            <div className="aspect-[362/483] overflow-hidden rounded-2xl">
              <img
                src="/images/2.jpg"
                alt="Structure moléculaire"
                className="w-full h-full object-cover rounded-2xl"
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
          <div className="rounded-2xl overflow-hidden">
            <div className="aspect-[362/483] overflow-hidden rounded-2xl">
              <img
                src="/images/3.jpg"
                alt="Cellule rose"
                className="w-full h-full object-cover rounded-2xl"
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
          <div className="rounded-2xl overflow-hidden">
            <div className="aspect-[362/483] overflow-hidden rounded-2xl">
              <img
                src="/images/4.jpg"
                alt="Scanner médical"
                className="w-full h-full object-cover rounded-2xl"
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
