"use client";

import { useEffect, useState, useCallback } from "react";

const API = "http://localhost:8000/api";

export default function Home() {
  const [capsules, setCapsules] = useState([]);
  const [error, setError] = useState("");

  const loadCapsules = useCallback(async () => {
    try {
      const res = await fetch(`${API}/capsules/`);
      const data = await res.json();
      setCapsules(data.results || data);
    } catch {
      setError("Can't reach the API. Is Django running?");
    }
  }, []);
  const [form, setForm] = useState({
    title: "", recipient_email: "", message: "", unlock_at: "",
  });
  const [sending, setSending] = useState(false);

  const setField = (key) => (e) =>
    setForm((f) => ({ ...f, [key]: e.target.value }));

  async function sealCapsule() {
    setError("");
    setSending(true);
    try {
      const res = await fetch(`${API}/capsules/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          unlock_at: new Date(form.unlock_at).toISOString(),
        }),
      });
      if (!res.ok) {
        const detail = await res.json();
        throw new Error(Object.values(detail).flat().join(" "));
      }
      setForm({ title: "", recipient_email: "", message: "", unlock_at: "" });
      await loadCapsules();
    } catch (e) {
      setError(e.message || "Something went wrong.");
    } finally {
      setSending(false);
    }
  }

  useEffect(() => {
    loadCapsules();
    const timer = setInterval(loadCapsules, 15000);
    return () => clearInterval(timer);
  }, [loadCapsules]);

  return (
    <main className="wrap">
      <h1>⏳ TimeCapsule</h1>
      <p>Write to the person you haven&apos;t met yet.</p>

      <section className="card">
        <h2>Seal a new capsule</h2>
        <label>Title</label>
        <input value={form.title} onChange={setField("title")} />
        <label>Deliver to (email)</label>
        <input type="email" value={form.recipient_email} onChange={setField("recipient_email")} />
        <label>Message</label>
        <textarea rows={4} value={form.message} onChange={setField("message")} />
        <label>Unlocks at</label>
        <input type="datetime-local" value={form.unlock_at} onChange={setField("unlock_at")} />
        <button onClick={sealCapsule} disabled={sending}>
          {sending ? "Sealing…" : "Seal capsule"}
        </button>
      </section>

      {error && <p className="error">{error}</p>}

      <section>
        <h2>The vault</h2>
        {capsules.map((c) => (
          <article key={c.id} className={`capsule ${c.status}`}>
            <strong>{c.title}</strong> <em>({c.status})</em>
            <p>{c.message}</p>
            <small>unlocks {new Date(c.unlock_at).toLocaleString()}</small>
          </article>
        ))}
      </section>
    </main>
  );
}