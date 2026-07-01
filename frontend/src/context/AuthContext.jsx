import { createContext, useContext, useEffect, useState } from 'react';
import client from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('ai_interviewer_token');
    if (!token) {
      setLoading(false);
      return;
    }
    client
      .get('/auth/me')
      .then((response) => setUser(response.data))
      .catch(() => {
        localStorage.removeItem('ai_interviewer_token');
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    const response = await client.post('/auth/login', { email, password });
    localStorage.setItem('ai_interviewer_token', response.data.access_token);
    setUser(response.data.user);
    return response.data;
  };

  const register = async (payload) => {
    const response = await client.post('/auth/register', payload);
    localStorage.setItem('ai_interviewer_token', response.data.access_token);
    setUser(response.data.user);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('ai_interviewer_token');
    setUser(null);
  };

  return <AuthContext.Provider value={{ user, loading, login, register, logout, setUser }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
