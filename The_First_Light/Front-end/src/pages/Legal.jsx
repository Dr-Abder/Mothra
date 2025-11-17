const Legal = () => {
  return (
    <div className="min-h-screen bg-beige py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Mentions Légales et RGPD
          </h1>
          <p className="text-lg text-gray-700">
            Dernière mise à jour : 17 novembre 2025
          </p>
        </div>

        {/* Éditeur du site */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            1. Éditeur du site
          </h2>
          <div className="space-y-2 text-gray-700">
            <p><strong>Nom du site :</strong> Mothra</p>
            <p><strong>Description :</strong> Plateforme d&apos;analyse dermatologique par intelligence artificielle</p>
            <p><strong>Contact RGPD :</strong> <a href="mailto:rgpd@mothra-health.com" className="text-gray-900 hover:underline font-semibold">rgpd@mothra-health.com</a></p>
            <p><strong>Support technique :</strong> <a href="mailto:support@mothra-health.com" className="text-gray-900 hover:underline font-semibold">support@mothra-health.com</a></p>
          </div>
        </section>

        {/* Hébergement */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            2. Hébergement
          </h2>
          <div className="space-y-2 text-gray-700">
            <p><strong>Hébergeur :</strong> À définir selon votre infrastructure</p>
            <p><strong>Localisation des serveurs :</strong> Union Européenne</p>
            <p className="text-sm text-gray-600 italic">
              Les données sont hébergées sur des serveurs sécurisés conformes aux normes RGPD
            </p>
          </div>
        </section>

        {/* Conformité RGPD */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            3. Conformité RGPD
          </h2>
          <p className="text-gray-700 mb-6">
            Mothra respecte le Règlement Général sur la Protection des Données (RGPD) et garantit
            les droits suivants à tous ses utilisateurs :
          </p>

          {/* Tableau de conformité */}
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse border border-gray-300">
              <thead className="bg-gray-light">
                <tr>
                  <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">
                    Principe RGPD
                  </th>
                  <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">
                    Statut
                  </th>
                  <th className="border border-gray-300 px-4 py-3 text-left font-semibold text-gray-900">
                    Implémentation
                  </th>
                </tr>
              </thead>
              <tbody className="text-gray-700">
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Consentement
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Checkbox obligatoire + validation backend
                  </td>
                </tr>
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Droit d&apos;accès
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Consultation de vos données via votre compte
                  </td>
                </tr>
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Droit de rectification
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Modification de vos informations personnelles
                  </td>
                </tr>
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Droit à l&apos;effacement
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Suppression compte + analyses + cascade automatique
                  </td>
                </tr>
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Portabilité
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Export JSON complet de toutes vos données
                  </td>
                </tr>
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Sécurité
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Bcrypt + JWT + isolation des fichiers utilisateur
                  </td>
                </tr>
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Transparence
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Politique de confidentialité accessible + page compte
                  </td>
                </tr>
                <tr className="hover:bg-beige">
                  <td className="border border-gray-300 px-4 py-3 font-medium">
                    Minimisation
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-black text-white">
                      ✅ Conforme
                    </span>
                  </td>
                  <td className="border border-gray-300 px-4 py-3">
                    Collecte uniquement des données strictement nécessaires
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Données collectées */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            4. Données personnelles collectées
          </h2>
          <div className="space-y-4 text-gray-700">
            <div>
              <h3 className="font-semibold text-lg mb-2">Données d&apos;identification :</h3>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Prénom et nom</li>
                <li>Adresse email</li>
                <li>Âge</li>
                <li>Sexe</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-2">Données de santé :</h3>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Photos dermatologiques</li>
                <li>Résultats d&apos;analyses et diagnostics</li>
                <li>Historique des consultations</li>
              </ul>
            </div>
            <div className="bg-gray-light border-l-4 border-gray-700 p-4 mt-4">
              <p className="text-sm text-gray-900">
                <strong>Important :</strong> Les données de santé sont des données sensibles
                bénéficiant d&apos;une protection renforcée selon l&apos;article 9 du RGPD.
              </p>
            </div>
          </div>
        </section>

        {/* Finalités du traitement */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            5. Finalités du traitement
          </h2>
          <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
            <li>Création et gestion de votre compte utilisateur</li>
            <li>Analyse dermatologique par intelligence artificielle</li>
            <li>Stockage sécurisé de vos résultats d&apos;analyse</li>
            <li>Amélioration des performances du modèle d&apos;IA (avec votre consentement)</li>
            <li>Communication relative à votre compte et nos services</li>
          </ul>
        </section>

        {/* Vos droits */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            6. Vos droits
          </h2>
          <div className="space-y-4 text-gray-700">
            <p className="font-medium">
              Conformément au RGPD, vous disposez des droits suivants :
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border-l-4 border-black pl-4">
                <h4 className="font-semibold mb-1">Droit d&apos;accès</h4>
                <p className="text-sm">Consultez vos données dans votre compte</p>
              </div>
              <div className="border-l-4 border-black pl-4">
                <h4 className="font-semibold mb-1">Droit de rectification</h4>
                <p className="text-sm">Modifiez vos informations personnelles</p>
              </div>
              <div className="border-l-4 border-black pl-4">
                <h4 className="font-semibold mb-1">Droit à l&apos;effacement</h4>
                <p className="text-sm">Supprimez votre compte et vos données</p>
              </div>
              <div className="border-l-4 border-black pl-4">
                <h4 className="font-semibold mb-1">Droit à la portabilité</h4>
                <p className="text-sm">Exportez vos données au format JSON</p>
              </div>
              <div className="border-l-4 border-black pl-4">
                <h4 className="font-semibold mb-1">Droit d&apos;opposition</h4>
                <p className="text-sm">Refusez certains traitements</p>
              </div>
              <div className="border-l-4 border-black pl-4">
                <h4 className="font-semibold mb-1">Droit à la limitation</h4>
                <p className="text-sm">Limitez le traitement de vos données</p>
              </div>
            </div>

            <div className="bg-gray-light p-4 rounded-lg mt-6">
              <p className="text-sm text-gray-900">
                <strong>Pour exercer vos droits :</strong> Rendez-vous dans votre
                <a href="/account" className="text-gray-900 hover:underline ml-1 mr-1 font-semibold">espace compte</a>
                ou contactez-nous à
                <a href="mailto:rgpd@mothra-health.com" className="text-gray-900 hover:underline ml-1 font-semibold">
                  rgpd@mothra-health.com
                </a>
              </p>
            </div>
          </div>
        </section>

        {/* Sécurité */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            7. Mesures de sécurité
          </h2>
          <div className="space-y-3 text-gray-700">
            <div className="flex items-start">
              <span className="text-green-600 mr-3 mt-1">✓</span>
              <p><strong>Chiffrement des mots de passe :</strong> Algorithme bcrypt avec salt</p>
            </div>
            <div className="flex items-start">
              <span className="text-green-600 mr-3 mt-1">✓</span>
              <p><strong>Authentification sécurisée :</strong> Tokens JWT avec expiration</p>
            </div>
            <div className="flex items-start">
              <span className="text-green-600 mr-3 mt-1">✓</span>
              <p><strong>Isolation des données :</strong> Chaque utilisateur a son propre espace de stockage</p>
            </div>
            <div className="flex items-start">
              <span className="text-green-600 mr-3 mt-1">✓</span>
              <p><strong>Connexion HTTPS :</strong> Chiffrement des communications</p>
            </div>
            <div className="flex items-start">
              <span className="text-green-600 mr-3 mt-1">✓</span>
              <p><strong>Politique de mots de passe forts :</strong> Minimum 8 caractères avec complexité</p>
            </div>
            <div className="flex items-start">
              <span className="text-green-600 mr-3 mt-1">✓</span>
              <p><strong>Suppression en cascade :</strong> Effacement complet des données associées</p>
            </div>
          </div>
        </section>

        {/* Conservation des données */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            8. Durée de conservation
          </h2>
          <div className="space-y-2 text-gray-700">
            <p>
              <strong>Données de compte actif :</strong> Conservées tant que votre compte existe
            </p>
            <p>
              <strong>Après suppression :</strong> Effacement immédiat et définitif de toutes vos données
            </p>
            <p>
              <strong>Logs de sécurité :</strong> Conservés 12 mois maximum pour la sécurité du service
            </p>
          </div>
        </section>

        {/* Cookies */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            9. Cookies et traceurs
          </h2>
          <div className="space-y-3 text-gray-700">
            <p>
              <strong>Cookies essentiels :</strong> Mothra utilise uniquement des cookies nécessaires
              au fonctionnement du service (authentification, session).
            </p>
            <p>
              <strong>Cookies analytiques :</strong> Aucun cookie de tracking ou analytique n&apos;est
              utilisé actuellement.
            </p>
            <div className="bg-gray-light p-4 rounded">
              <p className="text-sm text-gray-900">
                <strong>Stockage local :</strong> Votre token d&apos;authentification est stocké
                dans le localStorage de votre navigateur pour maintenir votre session.
              </p>
            </div>
          </div>
        </section>

        {/* Réclamations */}
        <section className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            10. Réclamations
          </h2>
          <div className="text-gray-700">
            <p className="mb-4">
              Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire
              une réclamation auprès de la CNIL :
            </p>
            <div className="bg-gray-light p-4 rounded">
              <p className="font-semibold text-gray-900">Commission Nationale de l&apos;Informatique et des Libertés (CNIL)</p>
              <p className="text-gray-700">3 Place de Fontenoy - TSA 80715</p>
              <p className="text-gray-700">75334 PARIS CEDEX 07</p>
              <p className="text-gray-700">Tél : 01 53 73 22 22</p>
              <p className="text-gray-700">
                Site web :
                <a
                  href="https://www.cnil.fr"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-900 hover:underline ml-1 font-semibold"
                >
                  www.cnil.fr
                </a>
              </p>
            </div>
          </div>
        </section>

        {/* Contact */}
        <section className="bg-black rounded-lg shadow-md p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">
            Questions ou demandes ?
          </h2>
          <p className="mb-4">
            Pour toute question concernant vos données personnelles ou l&apos;exercice de vos droits :
          </p>
          <div className="space-y-2">
            <p>
              <strong>Email RGPD :</strong>
              <a
                href="mailto:rgpd@mothra-health.com"
                className="underline ml-2 hover:text-gray-300"
              >
                rgpd@mothra-health.com
              </a>
            </p>
            <p>
              <strong>Support technique :</strong>
              <a
                href="mailto:support@mothra-health.com"
                className="underline ml-2 hover:text-gray-300"
              >
                support@mothra-health.com
              </a>
            </p>
          </div>
          <p className="mt-4 text-sm text-gray-300">
            Nous nous engageons à répondre à vos demandes dans un délai maximum de 30 jours.
          </p>
        </section>

        {/* Footer de la page */}
        <div className="text-center mt-8 text-gray-600 text-sm">
          <p>© 2025 Mothra - Tous droits réservés</p>
          <p className="mt-2">
            Dernière mise à jour de cette page : 17 novembre 2025
          </p>
        </div>
      </div>
    </div>
  );
};

export default Legal;
