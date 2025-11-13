import { Link } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { isAuthenticated } = useAuth();

  return (
    <nav className="navbar-bg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 -ml-10">
            <img src="/images/Logo.png" alt="Mothra Logo" className="w-10 h-10 object-contain" />
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            {isAuthenticated() ? (
              <>
                <Link
                  to="/account"
                  className="text-black hover:text-gray-600 transition-colors"
                >
                  Compte
                </Link>
                <Link
                  to="/dashboard"
                  className="text-black hover:text-gray-600 transition-colors"
                >
                  Dashboard
                </Link>
                <Link
                  to="/diagnostic"
                  className="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
                >
                  Diagnostic
                </Link>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-black hover:text-gray-600 transition-colors"
                >
                  Connexion
                </Link>
                <Link
                  to="/signup"
                  className="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
                >
                  Inscription
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-200"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden pb-4 space-y-3">
            {isAuthenticated() ? (
              <>
                <Link
                  to="/account"
                  className="block px-4 py-2 hover:bg-gray-200 rounded-lg"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Compte
                </Link>
                <Link
                  to="/dashboard"
                  className="block px-4 py-2 hover:bg-gray-200 rounded-lg"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  to="/diagnostic"
                  className="block px-4 py-2 bg-black text-white rounded-lg text-center"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Diagnostic
                </Link>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-4 py-2 hover:bg-gray-200 rounded-lg"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Connexion
                </Link>
                <Link
                  to="/signup"
                  className="block px-4 py-2 bg-black text-white rounded-lg text-center"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Inscription
                </Link>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
