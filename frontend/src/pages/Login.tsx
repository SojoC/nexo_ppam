import React, { useState } from 'react';
import { login } from '../api';

interface Props {
  onLogin: (token: string) => void;
}

function Login({ onLogin }: Props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const data = await login(username, password);
      onLogin(data.access_token);
    } catch (err) {
      setError('Credenciales incorrectas');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Iniciar sesión</h2>
      <input
        type="text"
        placeholder="Usuario"
        value={username}
        onChange={e => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Contraseña"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />
      <button type="submit">Entrar</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </form>
  );
}

export default Login;
