/// <reference types="vite/client" />
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const BASE = `${API_URL}${API_PREFIX}`;

export async function login(username: string, password: string) {
  const body = new URLSearchParams({ username, password });
  const res = await fetch(`${BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Login failed ${res.status}: ${text}`);
  }
  return res.json();
}

export async function getContacts(token: string) {
  const res = await fetch(`${BASE}/contacts`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('No se pudieron cargar contactos');
  return res.json();
}

export async function getStats(token: string) {
  const res = await fetch(`${BASE}/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('No se pudieron cargar estadísticas');
  return res.json();
}

export async function getMessages(token: string, contactId: number) {
  const res = await fetch(`${BASE}/messages/${contactId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('No se pudieron cargar mensajes');
  return res.json();
}

export async function sendMessage(token: string, contactId: number, text: string) {
  const res = await fetch(`${BASE}/messages/${contactId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error('No se pudo enviar el mensaje');
  return res.json();
}
