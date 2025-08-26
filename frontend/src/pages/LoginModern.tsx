
import React, { useState } from 'react';
import { login as apiLogin } from '../api';

interface Props {
  onLogin: (token: string) => void;
}

function Login({ onLogin }: Props) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [show, setShow] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
  const data = await apiLogin(username, password);
      onLogin(data.access_token);
    } catch (err: any) {
      setError(err.message || 'Error en inicio de sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-bg">
      <header className="login-header">
        <div className="brand">
          <div className="logo">NP</div>
          <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google logo" style={{height:32, marginLeft:12}} />
          <div>
            <div className="title">Nexo PPAM</div>
            <div className="subtitle">Panel de acceso</div>
          </div>
        </div>
        <div className="subtitle">v1 • FastAPI</div>
      </header>
      <main>
        <section className="card" aria-labelledby="title">
          <h1 id="title">Iniciar sesión</h1>
          <p className="lead">Bienvenido. Usa tus credenciales de Nexo PPAM para continuar.</p>
          <form onSubmit={handleSubmit} className="login-form">
            <div className="control">
              <label htmlFor="user">Usuario o correo</label>
              <input id="user" name="username" type="text" placeholder="p. ej. admin" autoComplete="username" required value={username} onChange={e => setUsername(e.target.value)} />
            </div>
            <div className="control">
              <label htmlFor="pass">Contraseña</label>
              <input id="pass" name="password" type={show ? 'text' : 'password'} placeholder="••••••••" autoComplete="current-password" required value={password} onChange={e => setPassword(e.target.value)} />
              <button type="button" className="toggle" aria-label="Mostrar u ocultar contraseña" onClick={() => setShow(s => !s)}>{show ? '🙈' : '👁️'}</button>
            </div>
            <div className="row">
              <button className="btn" type="submit" disabled={loading}>
                {loading ? <span className="spinner"></span> : <span>Entrar</span>}
              </button>
            </div>
            <div className="hint">Tip: con la base de datos de prueba, usa <code>admin / admin</code>.</div>
            {error && <div className="alert error">{error}</div>}
          </form>
        </section>
      </main>
      <footer>
        © {new Date().getFullYear()} Nexo PPAM — Interfaz moderna en azul oscuro.
      </footer>
    </div>
  );
}

export default Login;
