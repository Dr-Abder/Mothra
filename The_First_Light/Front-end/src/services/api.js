import axios from 'axios';

//  Utilise la variable d'environnement avec fallback sur localhost pour le dev
const API_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : 'http://localhost:8000/api/v1';

// Créer une instance axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token à chaque requête
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs d'authentification
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expiré ou invalide
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ==================== AUTH ====================

export const auth = {
  // Inscription
  signup: async (userData) => {
    const response = await api.post('/auth/signup', userData);
    return response.data;
  },

  // Connexion
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  // Déconnexion
  logout: async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },
};

// ==================== USERS ====================

export const users = {
  // Récupérer mon profil
  getProfile: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },

  // Mettre à jour mon profil
  updateProfile: async (userData) => {
    const response = await api.put('/users/me', userData);
    return response.data;
  },

  // Supprimer mon compte
  deleteAccount: async () => {
    const response = await api.delete('/users/me');
    return response.data;
  },

  // Export RGPD
  exportData: async () => {
    const response = await api.get('/users/me/data-export');
    return response.data;
  },

  // Supprimer toutes mes analyses
  deleteAllAnalyses: async () => {
    const response = await api.delete('/users/me/analyses');
    return response.data;
  },
};

// ==================== ANALYSES ====================

export const analyses = {
  // Récupérer toutes mes analyses
  getAll: async () => {
    const response = await api.get('/analyses');
    return response.data;
  },

  // Récupérer une analyse par ID
  getById: async (id) => {
    const response = await api.get(`/analyses/${id}`);
    return response.data;
  },

  // Supprimer une analyse
  delete: async (id) => {
    const response = await api.delete(`/analyses/${id}`);
    return response.data;
  },
};

// ==================== PREDICTION ====================

export const predict = {
  // Analyser une image
  analyze: async (imageFile) => {
    const formData = new FormData();
    formData.append('file', imageFile);

    const response = await api.post('/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

// ==================== IMAGES ====================

export const images = {
  // Récupérer l'image d'une analyse
  getAnalysisImage: (analyseId) => {
    const token = localStorage.getItem('token');
    return `${API_URL}/images/analyses/${analyseId}/image?token=${token}`;
  },

  // Supprimer l'image d'une analyse
  deleteAnalysisImage: async (analyseId) => {
    const response = await api.delete(`/images/analyses/${analyseId}/image`);
    return response.data;
  },

  // Statistiques de stockage
  getStorageStats: async () => {
    const response = await api.get('/images/storage/stats');
    return response.data;
  },
};

export default api;
