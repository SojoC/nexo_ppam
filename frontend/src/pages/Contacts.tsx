import React, { useEffect, useState } from 'react';
import { getContacts, getMessages, sendMessage } from '../api';

interface Contact {
  id: number;
  name: string;
}

interface Message {
  id: number;
  text: string;
  sender: string;
  timestamp: string;
}

interface Props {
  token: string;
}

function Contacts({ token }: Props) {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [selected, setSelected] = useState<Contact | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState('');

  useEffect(() => {
    getContacts(token).then(setContacts);
  }, [token]);

  useEffect(() => {
    if (selected) {
      getMessages(token, selected.id).then(setMessages);
    }
  }, [selected, token]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selected || !text) return;
    await sendMessage(token, selected.id, text);
    setText('');
    const msgs = await getMessages(token, selected.id);
    setMessages(msgs);
  };

  return (
    <div style={{ display: 'flex' }}>
      <ul style={{ minWidth: 200 }}>
        {contacts.map(c => (
          <li key={c.id}>
            <button onClick={() => setSelected(c)}>{c.name}</button>
          </li>
        ))}
      </ul>
      <div style={{ flex: 1, marginLeft: 20 }}>
        {selected ? (
          <>
            <h3>Mensajes con {selected.name}</h3>
            <div style={{ height: 200, overflowY: 'auto', border: '1px solid #ccc', marginBottom: 10 }}>
              {messages.map(m => (
                <div key={m.id}>
                  <b>{m.sender}:</b> {m.text} <small>{m.timestamp}</small>
                </div>
              ))}
            </div>
            <form onSubmit={handleSend}>
              <input
                value={text}
                onChange={e => setText(e.target.value)}
                placeholder="Escribe un mensaje"
                required
              />
              <button type="submit">Enviar</button>
            </form>
          </>
        ) : (
          <div>Selecciona un contacto</div>
        )}
      </div>
    </div>
  );
}

export default Contacts;
