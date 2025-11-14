import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Signup = () => {
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: '',
    age: '',
    sex: 'homme',
    consent_rgpd: false,
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
    setError('');
  };

  const validateForm = () => {
    if (!formData.first_name || !formData.last_name) {
      setError('Nom et prénom sont requis');
      return false;
    }

    if (!formData.email.includes('@')) {
      setError('Email invalide');
      return false;
    }

    // Validation stricte du mot de passe (conforme au back-end)
    if (formData.password.length < 8) {
      setError('Le mot de passe doit contenir au moins 8 caractères');
      return false;
    }

    const passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
    if (!passwordRegex.test(formData.password)) {
      setError('Le mot de passe doit contenir : 1 majuscule, 1 minuscule, 1 chiffre et 1 caractère spécial (#?!@$%^&*-)');
      return false;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return false;
    }

    if (!formData.age || formData.age < 1 || formData.age > 120) {
      setError('Âge invalide');
      return false;
    }

    if (!formData.consent_rgpd) {
      setError('Vous devez accepter la politique de confidentialité');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!validateForm()) {
      setLoading(false);
      return;
    }

    // Préparer les données pour l'API (sans confirmPassword)
    const { confirmPassword, ...apiData } = formData;
    apiData.age = parseInt(apiData.age);

    const result = await signup(apiData);

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <h2 className="text-4xl font-bold mb-2">Inscription</h2>
          <p className="text-gray-600">
            Créez votre compte pour commencer vos diagnostics
          </p>
        </div>

        {/* Form */}
        <form className="mt-8 space-y-6 bg-white p-8 rounded-2xl shadow-lg" onSubmit={handleSubmit}>
          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Prénom */}
            <div>
              <label htmlFor="first_name" className="block text-sm font-semibold mb-2">
                Prénom *
              </label>
              <input
                id="first_name"
                name="first_name"
                type="text"
                required
                value={formData.first_name}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent"
                placeholder="Jean"
              />
            </div>

            {/* Nom */}
            <div>
              <label htmlFor="last_name" className="block text-sm font-semibold mb-2">
                Nom *
              </label>
              <input
                id="last_name"
                name="last_name"
                type="text"
                required
                value={formData.last_name}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent"
                placeholder="Dupont"
              />
            </div>
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-semibold mb-2">
              Email *
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent"
              placeholder="jean.dupont@email.com"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-semibold mb-2">
                Mot de passe *
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent"
                placeholder="••••••••"
              />
              <p className="text-xs text-gray-500 mt-1">Minimum 8 caractères</p>
            </div>

            {/* Confirm Password */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-semibold mb-2">
                Confirmer le mot de passe *
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Âge */}
            <div>
              <label htmlFor="age" className="block text-sm font-semibold mb-2">
                Âge *
              </label>
              <input
                id="age"
                name="age"
                type="number"
                required
                min="1"
                max="120"
                value={formData.age}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent"
                placeholder="30"
              />
            </div>

            {/* Sexe */}
            <div>
              <label htmlFor="sex" className="block text-sm font-semibold mb-2">
                Sexe *
              </label>
              <select
                id="sex"
                name="sex"
                required
                value={formData.sex}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent"
              >
                <option value="homme">Homme</option>
                <option value="femme">Femme</option>
                <option value="autre">Autre</option>
              </select>
            </div>
          </div>

          {/* RGPD Consent */}
          <div className="flex items-start space-x-3">
            <input
              id="consent_rgpd"
              name="consent_rgpd"
              type="checkbox"
              checked={formData.consent_rgpd}
              onChange={handleChange}
              className="w-5 h-5 mt-1 border-gray-300 rounded focus:ring-black"
            />
            <label htmlFor="consent_rgpd" className="text-sm text-gray-700">
              J'accepte la politique de confidentialité et consens au traitement
              de mes données personnelles conformément au RGPD. *
            </label>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-colors ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-black hover:bg-gray-800'
            }`}
          >
            {loading ? (
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
                Création du compte...
              </span>
            ) : (
              "S'inscrire"
            )}
          </button>

          {/* Login Link */}
          <div className="text-center pt-4">
            <p className="text-gray-600">
              Vous avez déjà un compte?{' '}
              <Link to="/login" className="font-semibold text-black hover:underline">
                Connectez-vous
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Signup;
