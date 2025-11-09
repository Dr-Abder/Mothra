import { createContext, useContext, useState, useEffect } from 'react';
import { auth as authAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Charger l'utilisateur depuis le localStorage au démarrage
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  // Connexion
  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });

      // Sauvegarder le token et l'utilisateur
      setToken(response.access_token);
      setUser({
        id: response.user_id,
        email: email,
      });

      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify({
        id: response.user_id,
        email: email,
      }));

      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Erreur de connexion',
      };
    }
  };

  // Inscription
  const signup = async (userData) => {
    try {
      const response = await authAPI.signup(userData);

      // Sauvegarder le token et l'utilisateur
      setToken(response.access_token);
      setUser({
        id: response.user_id,
        email: userData.email,
        firstName: userData.first_name,
        lastName: userData.last_name,
      });

      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify({
        id: response.user_id,
        email: userData.email,
        firstName: userData.first_name,
        lastName: userData.last_name,
      }));

      return { success: true };
    } catch (error) {
      console.error('Signup error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Erreur lors de l\'inscription',
      };
    }
  };

  // Déconnexion
  const logout = async () => {
    await authAPI.logout();
    setUser(null);
    setToken(null);
  };

  // Vérifier si l'utilisateur est connecté
  const isAuthenticated = () => {
    return token !== null && user !== null;
  };

  const value = {
    user,
    token,
    loading,
    login,
    signup,
    logout,
    isAuthenticated,
    setUser, // Pour mettre à jour l'utilisateur après modification du profil
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Hook personnalisé pour utiliser le contexte
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
