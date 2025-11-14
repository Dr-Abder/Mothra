import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { users as usersAPI } from '../services/api';

const Account = () => {
  const navigate = useNavigate();
  const { user: authUser, setUser, logout } = useAuth();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      setLoading(true);
      const data = await usersAPI.getProfile();
      setUserData(data);
      setError('');
    } catch (err) {
      console.error('Erreur lors du chargement du profil:', err);
      setError('Impossible de charger vos informations');
    } finally {
      setLoading(false);
    }
  };

  const handleExportData = async () => {
    try {
      const exportData = await usersAPI.exportData();

      // Créer un fichier JSON et le télécharger
      const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: 'application/json',
      });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `mothra-export-${new Date().toISOString()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      alert('Export réussi ! Vos données ont été téléchargées.');
    } catch (err) {
      console.error('Erreur lors de l\'export:', err);
      alert('Erreur lors de l\'export de vos données');
    }
  };

  const handleDeleteAccount = async () => {
    const confirmed = window.confirm(
      'Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible et supprimera toutes vos données (compte, analyses, images).'
    );

    if (!confirmed) return;

    const doubleConfirm = window.prompt(
      'Pour confirmer, tapez "SUPPRIMER" en majuscules :'
    );

    if (doubleConfirm !== 'SUPPRIMER') {
      alert('Suppression annulée');
      return;
    }

    try {
      await usersAPI.deleteAccount();
      alert('Votre compte a été supprimé définitivement.');
      await logout();
      navigate('/');
    } catch (err) {
      console.error('Erreur lors de la suppression:', err);
      alert('Erreur lors de la suppression du compte');
    }
  };

  const handleDeleteAllAnalyses = async () => {
    const confirmed = window.confirm(
      'Êtes-vous sûr de vouloir supprimer toutes vos analyses ? Cette action est irréversible.'
    );

    if (!confirmed) return;

    try {
      await usersAPI.deleteAllAnalyses();
      alert('Toutes vos analyses ont été supprimées.');
    } catch (err) {
      console.error('Erreur lors de la suppression:', err);
      alert('Erreur lors de la suppression des analyses');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-black mb-4"></div>
          <p className="text-lg">Chargement de votre profil...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-700 mb-4">{error}</p>
          <button
            onClick={loadUserData}
            className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div>
              <h1 className="text-5xl md:text-6xl font-bold mb-4">
                {userData?.first_name} {userData?.last_name}
              </h1>
              <div className="space-y-2 text-xl text-gray-700">
                <p>
                  <span className="font-semibold">Email:</span> {userData?.email}
                </p>
                <p>
                  <span className="font-semibold">Âge:</span> {userData?.age} ans
                </p>
                <p>
                  <span className="font-semibold">Sexe:</span>{' '}
                  {userData?.sex === 'homme' ? 'Homme' : userData?.sex === 'femme' ? 'Femme' : 'Autre'}
                </p>
                <p className="text-sm text-gray-500 pt-2">
                  Membre depuis le{' '}
                  {userData?.created_at && new Date(userData.created_at).toLocaleDateString('fr-FR')}
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <button
                onClick={() => navigate('/diagnostic')}
                className="w-full sm:w-auto px-8 py-4 bg-black text-white rounded-lg font-semibold hover:bg-gray-800 transition-colors"
              >
                Effectuez un diagnostic
              </button>

              <button
                onClick={async () => {
                  await logout();
                  navigate('/login');
                }}
                className="w-full sm:w-auto ml-0 sm:ml-4 px-8 py-4 bg-gray-300 text-black rounded-lg font-semibold hover:bg-gray-400 transition-colors"
              >
                Se déconnecter
              </button>
            </div>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="aspect-square rounded-2xl bg-gray-200 overflow-hidden">
              <img
                src="/images/M3.jpg"
                alt="Profil"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>

        {/* RGPD Section */}
        <section className="mt-20 max-w-4xl">
          <h2 className="text-4xl font-bold mb-8">
            Protection de vos données
          </h2>

          <div className="space-y-6 text-lg text-gray-700 leading-relaxed">
            <p>
              Votre vie privée est notre priorité. Toutes les données que vous nous confiez 
              photos, informations personnelles, résultats de diagnostic ou autres 
              sont strictement protégées et ne sont jamais partagées avec des tiers.
              Vous gardez un contrôle total sur vos données :
            </p>

            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3"></div>
                <p>
                  <span className="font-semibold">Chiffrement des données :</span>{' '}
                  Toutes vos informations médicales et personnelles sont chiffrées
                  et stockées de manière sécurisée.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3"></div>
                <p>
                  <span className="font-semibold">Accès restreint :</span> Vous
                  êtes le seul à avoir accès à vos analyses. Aucun tiers ne peut
                  consulter vos données sans votre consentement explicite.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3"></div>
                <p>
                  <span className="font-semibold">Droit à l'effacement :</span>{' '}
                  Vous pouvez à tout moment demander la suppression définitive de
                  toutes vos données de nos serveurs.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3"></div>
                <p>
                  <span className="font-semibold">Portabilité :</span> Vous avez
                  le droit d'exporter l'intégralité de vos données médicales dans
                  un format lisible.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3"></div>
                <p>
                  <span className="font-semibold">Utilisation transparente :</span>{' '}
                  Vos images ne sont utilisées que pour générer vos diagnostics.
                  Nous ne partageons jamais vos données avec des tiers sans votre
                  accord.
                </p>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 rounded-full bg-black flex-shrink-0 mt-3"></div>
                <p>
                  <span className="font-semibold">Conformité RGPD :</span> Notre
                  système est entièrement conforme au RGPD et nous respectons tous
                  vos droits en matière de protection des données personnelles.
                </p>
              </div>
            </div>
          </div>

          {/* RGPD Actions */}
          <div className="mt-12 space-y-4">
            <h3 className="text-2xl font-bold mb-6">Vos droits RGPD</h3>

            <div className="bg-white rounded-2xl p-6 shadow-lg space-y-4">
              <button
                onClick={handleExportData}
                className="w-full px-6 py-4 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition-colors text-left flex items-center justify-between"
              >
                <div>
                  <p className="font-semibold">Exporter mes données</p>
                  <p className="text-sm opacity-90">
                    Télécharger toutes vos données au format JSON (portabilité RGPD)
                  </p>
                </div>
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                  />
                </svg>
              </button>

              <button
                onClick={handleDeleteAllAnalyses}
                className="w-full px-6 py-4 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition-colors text-left flex items-center justify-between"
              >
                <div>
                  <p className="font-semibold">Supprimer toutes mes analyses</p>
                  <p className="text-sm opacity-90">
                    Supprime toutes vos analyses mais conserve votre compte
                  </p>
                </div>
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
              </button>

              <button
                onClick={handleDeleteAccount}
                className="w-full px-6 py-4 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition-colors text-left flex items-center justify-between"
              >
                <div>
                  <p className="font-semibold">Supprimer mon compte définitivement</p>
                  <p className="text-sm opacity-90">
                    ! Action irréversible - Supprime toutes vos données
                  </p>
                </div>
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </button>
            </div>
          </div>

          <p className="pt-8 text-gray-600">
            Pour toute question concernant vos données ou pour exercer vos
            droits, vous pouvez nous contacter à{' '}
            <a
              href="mailto:rgpd@mothra-health.com"
              className="font-semibold underline hover:text-black"
            >
              rgpd@mothra-health.com
            </a>
          </p>
        </section>
      </div>
    </div>
  );
};

export default Account;
