import React, { useEffect, useState } from 'react';
import { getStats } from '../api';

interface Props {
  token: string;
}

function Stats({ token }: Props) {
  const [stats, setStats] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    getStats(token)
      .then(setStats)
      .catch(() => setError('No se pudieron cargar las estadísticas'));
  }, [token]);

  if (error) return <div>{error}</div>;
  if (!stats) return <div>Cargando...</div>;

  return (
    <div>
      <h2>Estadísticas</h2>
      <pre>{JSON.stringify(stats, null, 2)}</pre>
    </div>
  );
}

export default Stats;
