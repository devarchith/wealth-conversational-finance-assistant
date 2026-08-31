"use client";

import { FormEvent, useState } from "react";
import { api } from "@/lib/api";

export default function ForgotPassword() {
  const [email, setEmail] = useState(""); const [message, setMessage] = useState(""); const [error, setError] = useState("");
  async function submit(e: FormEvent) { e.preventDefault(); setError(""); try { const result = await api<{message:string}>("/auth/password-reset/request", {method:"POST", body:JSON.stringify({email})}); setMessage(result.message); } catch (cause) { setError(cause instanceof Error ? cause.message : "Unable to request reset"); } }
  return <main className="form-shell"><p className="eyebrow">Account recovery</p><h1>Reset your password.</h1><div className="form-card"><form onSubmit={submit}><div className="field"><label htmlFor="email">Email</label><input id="email" type="email" required value={email} onChange={e=>setEmail(e.target.value)} /></div>{message && <p className="success">{message}</p>}{error && <p className="error">{error}</p>}<button className="button">Send reset link</button></form></div></main>;
}

