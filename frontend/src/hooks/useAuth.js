import { useState, useEffect } from 'react';

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Verificar se o usuário está autenticado no localStorage
    const checkAuth = () => {
      const authStatus = localStorage.getItem('isAuthenticated');
      const username = localStorage.getItem('username');
      
      if (authStatus === 'true' && username) {
        setIsAuthenticated(true);
        setUser({ username });
      } else {
        setIsAuthenticated(false);
        setUser(null);
      }
      
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = (success) => {
    if (success) {
      setIsAuthenticated(true);
      const username = localStorage.getItem('username');
      setUser({ username });
    }
  };

  const logout = () => {
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('username');
    setIsAuthenticated(false);
    setUser(null);
  };

  return {
    isAuthenticated,
    isLoading,
    user,
    login,
    logout
  };
};
