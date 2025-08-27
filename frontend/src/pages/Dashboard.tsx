import React, { useEffect, useState } from "react";
import { useAuth } from "../auth";
import { getStats, getContacts } from "../api";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { token, logout } = useAuth();
  const [stats, setStats] = useState<any>(null);
  const [contacts, setContacts] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const s = await getStats(token!);
        const c = await getContacts(token!);
        if (!mounted) return;
        setStats(s);
        setContacts(c);
      } catch (e: any) {
        setError(e.message || "Error cargando datos");
        if (String(e).includes("401")) logout();
      }
    })();
    return () => { mounted = false; };
  }, [token, logout]);

  return (
    <div className="p-4">
      <h1>Dashboard</h1>
      {error && <div className="alert error">{error}</div>}
      <section>
        <h2>Stats</h2>
        <pre>{JSON.stringify(stats, null, 2)}</pre>
      </section>
      <section>
        <h2>Contactos</h2>
        <ul>
          {contacts.map((c: any) => (
            <li key={c.id}>
              <Link to={`/chat/${c.id}`}>{c.name ?? `Contacto ${c.id}`}</Link>
            </li>
          ))}
        </ul>
      </section>
      <button onClick={logout}>Cerrar sesión</button>
    </div>
  );
}
