import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/LoginModern';
import Contacts from './pages/Contacts';
import Stats from './pages/Stats';
import { useAuth } from './auth';

export default function App() {
  const { token } = useAuth();
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/contacts" element={token ? <Contacts /> : <Navigate to="/login" replace />} />
      <Route path="/stats" element={token ? <Stats /> : <Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to={token ? '/contacts' : '/login'} replace />} />
    </Routes>
  );
}
