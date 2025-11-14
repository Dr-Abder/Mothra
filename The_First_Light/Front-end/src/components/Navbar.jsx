import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { isAuthenticated } = useAuth();

  return (
    <nav className="navbar-bg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Desktop Layout */}
        <div className="hidden md:flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <img src="/images/Logo.png" alt="Mothra Logo" className="w-10 h-10 object-contain" />
          </Link>

          {/* Desktop Menu */}
          <div className="flex items-center space-x-8">
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
                  className="text-black hover:text-gray-600 transition-colors"
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
        </div>

        {/* Mobile Layout */}
        <div className="md:hidden py-4 flex justify-between items-center">
          {/* Logo à gauche */}
          <Link to="/" className="flex items-center pt-">
            <img src="/images/Logo.png" alt="Mothra Logo" className="w-24 h-24 object-contain" />
          </Link>

          {/* Boutons empilés verticalement à droite */}
          <div className="flex flex-col space-y-1">
            {isAuthenticated() ? (
              <>
                <Link
                  to="/account"
                  className="block px-6 py-2 text-right hover:bg-gray-200 rounded-lg transition-colors"
                >
                  Compte
                </Link>
                <Link
                  to="/dashboard"
                  className="block px-6 py-2 text-right hover:bg-gray-200 rounded-lg transition-colors"
                >
                  Dashboard
                </Link>
                <Link
                  to="/diagnostic"
                  className="block px-6 py-2 text-right hover:bg-gray-800 rounded-lg transition-colors"
                >
                  Diagnostic
                </Link>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-6 py-2 text-center hover:bg-gray-200 rounded-lg transition-colors"
                >
                  Connexion
                </Link>
                <Link
                  to="/signup"
                  className="block px-6 py-2 bg-black text-white rounded-lg text-center hover:bg-gray-800 transition-colors"
                >
                  Inscription
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
