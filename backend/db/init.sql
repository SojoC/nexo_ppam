-- backend/db/init.sql
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Wrapper IMMUTABLE para indexar sobre unaccent
CREATE OR REPLACE FUNCTION public.immutable_unaccent(text)
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $$
  SELECT public.unaccent('unaccent', $1)::text;
$$;

-- Tabla contacts
CREATE TABLE IF NOT EXISTS contacts (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR,
  telefono VARCHAR,
  circuito VARCHAR,
  congregacion VARCHAR,
  territorio VARCHAR,
  privilegios VARCHAR,
  metadata JSON
);

-- Índices GIN trigram con wrapper
CREATE INDEX IF NOT EXISTS idx_contacts_nombre_trgm
  ON contacts USING gin (immutable_unaccent(nombre) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_contacts_congregacion_trgm
  ON contacts USING gin (immutable_unaccent(congregacion) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_contacts_circuito_trgm
  ON contacts USING gin (immutable_unaccent(circuito) gin_trgm_ops);

-- Datos demo (opcionales)
INSERT INTO contacts (nombre, telefono, circuito, congregacion, territorio, privilegios, metadata)
SELECT * FROM (VALUES
('Carlos Sojo', '0413-370-5540', 'Monagas 1', 'El Parque', 'T-01', 'publicador', '{"tags":["demo","mg1"]}'),
('Ana Pérez', '0412-111-1111', 'Monagas 1', 'El Parque', 'T-02', 'pionero', '{"tags":["demo","mg1"]}'),
('Luis Gómez', '0414-222-2222', 'Monagas 2', 'San José', 'T-05', 'auxiliar', '{"tags":["demo"]}')
) AS t(nombre, telefono, circuito, congregacion, territorio, privilegios, metadata)
WHERE NOT EXISTS (SELECT 1 FROM contacts);
