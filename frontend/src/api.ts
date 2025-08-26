/// <reference types="vite/client" />
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function login(username: string, password: string) {
  const res = await fetch(`${API_URL}/api/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

export async function getContacts(token: string) {
  const res = await fetch(`${API_URL}/api/contacts`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch contacts');
  return res.json();
}

export async function getStats(token: string) {
  const res = await fetch(`${API_URL}/api/stats`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch stats');
  return res.json();
}

export async function getMessages(token: string, contactId: number) {
  const res = await fetch(`${API_URL}/api/messages/${contactId}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch messages');
  return res.json();
}

export async function sendMessage(token: string, contactId: number, text: string) {
  const res = await fetch(`${API_URL}/api/messages/${contactId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ text })
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}
