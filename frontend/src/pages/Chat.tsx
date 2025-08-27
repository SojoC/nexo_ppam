import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../auth";
import { getMessages, sendMessage } from "../api";

export default function Chat() {
  const { id } = useParams<{ id: string }>();
  const contactId = Number(id);
  const { token, logout } = useAuth();
  const [msgs, setMsgs] = useState<any[]>([]);
  const [text, setText] = useState("");
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const m = await getMessages(token!, contactId);
      setMsgs(m);
    } catch (e: any) {
      setError(e.message || "Error");
      if (String(e).includes("401")) logout();
    }
  };

  useEffect(() => { load(); /* eslint-disable-next-line */ }, [contactId]);

  const onSend = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await sendMessage(token!, contactId, text);
      setText("");
      await load();
    } catch (e: any) {
      setError(e.message || "No se pudo enviar");
    }
  };

  return (
    <div className="p-4">
      <h1>Chat con #{contactId}</h1>
      {error && <div className="alert error">{error}</div>}
      <div className="messages">
        {msgs.map((m, i) => (
          <div key={i} className="bubble">{m.text ?? JSON.stringify(m)}</div>
        ))}
      </div>
      <form onSubmit={onSend} className="row gap-2">
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Escribe un mensaje" />
        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}
