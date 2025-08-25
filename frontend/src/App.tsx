import React, { useState } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import Contacts from './pages/Contacts';
import Stats from './pages/Stats';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const navigate = useNavigate();

  const handleLogin = (t: string) => {
    setToken(t);
    localStorage.setItem('token', t);
    navigate('/contacts');
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div>
      {token && (
        <nav>
          <button onClick={() => navigate('/contacts')}>Contactos</button>
          <button onClick={() => navigate('/stats')}>Estadísticas</button>
          <button onClick={handleLogout}>Cerrar sesión</button>
        </nav>
      )}
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/contacts" element={token ? <Contacts token={token} /> : <Navigate to="/login" />} />
        <Route path="/stats" element={token ? <Stats token={token} /> : <Navigate to="/login" />} />
        <Route path="*" element={<Navigate to={token ? "/contacts" : "/login"} />} />
      </Routes>
    </div>
  );
}

export default App;
