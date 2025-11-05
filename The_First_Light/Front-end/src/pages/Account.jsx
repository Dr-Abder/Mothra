import { Link } from 'react-router-dom';

const Account = () => {
  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div>
              <h1 className="text-5xl md:text-6xl font-bold mb-4">
                Abbderrahmane Ghomed
              </h1>
              <p className="text-xl text-gray-700">
                Le patient est un homme âgé de 20 ans présentant un phototype
                cutané normal
              </p>
            </div>

            <Link
              to="/diagnostic"
              className="inline-block px-8 py-4 bg-black text-white rounded-lg font-semibold hover:bg-gray-800 transition-colors"
            >
              Effectuez un diagnostic
            </Link>
          </div>

          {/* Right Image - Vitruvian Man */}
          <div className="relative">
            <div className="aspect-square rounded-2xl bg-gray-200 overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1530210124550-912dc1381cb8?w=800&h=800&fit=crop"
                alt="Homme de Vitruve"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>

        {/* Data Protection Section */}
        <section className="mt-20 max-w-4xl">
          <h2 className="text-4xl font-bold mb-8">
            Protection de vos données
          </h2>

          <div className="space-y-6 text-lg text-gray-700 leading-relaxed">
            <p>
              Chez Mothra, nous prenons la protection de vos données personnelles
              très au sérieux. Toutes les informations que vous nous confiez sont
              traitées avec le plus grand soin et dans le strict respect de la
              réglementation RGPD (Règlement Général sur la Protection des
              Données).
            </p>

            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
                <p>
                  <span className="font-semibold">Chiffrement des données :</span>{" "}
                  Toutes vos informations médicales et personnelles sont chiffrées
                  et stockées de manière sécurisée.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
                <p>
                  <span className="font-semibold">Accès restreint :</span> Vous
                  êtes le seul à avoir accès à vos analyses. Aucun tiers ne peut
                  consulter vos données sans votre consentement explicite.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
                <p>
                  <span className="font-semibold">Droit à l'effacement :</span>{" "}
                  Vous pouvez à tout moment demander la suppression définitive de
                  toutes vos données de nos serveurs.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
                <p>
                  <span className="font-semibold">Portabilité :</span> Vous avez
                  le droit d'exporter l'intégralité de vos données médicales dans
                  un format lisible.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
                <p>
                  <span className="font-semibold">Utilisation transparente :</span>{" "}
                  Vos images ne sont utilisées que pour générer vos diagnostics.
                  Nous ne partageons jamais vos données avec des tiers sans votre
                  accord.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-black flex-shrink-0 mt-1"></div>
                <p>
                  <span className="font-semibold">Conformité RGPD :</span> Notre
                  système est entièrement conforme au RGPD et nous respectons tous
                  vos droits en matière de protection des données personnelles.
                </p>
              </div>
            </div>

            <p className="pt-4">
              Pour toute question concernant vos données ou pour exercer vos
              droits, vous pouvez nous contacter à{" "}
              <a
                href="mailto:rgpd@mothra-health.com"
                className="font-semibold underline hover:text-black"
              >
                rgpd@mothra-health.com
              </a>
            </p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Account;
