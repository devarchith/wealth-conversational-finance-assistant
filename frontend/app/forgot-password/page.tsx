"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { Icon } from "@/components/Icon";

export default function ForgotPassword() {
  const [email, setEmail] = useState(""); const [message, setMessage] = useState(""); const [error, setError] = useState(""); const [busy,setBusy]=useState(false);
  async function submit(e: FormEvent) { e.preventDefault(); setError(""); setMessage(""); setBusy(true); try { const result = await api<{message:string}>("/auth/password-reset/request", {method:"POST", body:JSON.stringify({email})}); setMessage(result.message); } catch (cause) { setError(cause instanceof Error ? cause.message : "Unable to request reset"); } finally { setBusy(false); } }
  return <main className="narrow-page"><div className="back-link"><Link href="/login">← Back to log in</Link></div><section className="form-card recovery-card"><span className="form-icon" aria-hidden="true"><Icon name="profile"/></span><p className="eyebrow">Account recovery</p><h1>Reset your password</h1><p className="muted">Enter the email connected to your workspace. If it matches an account, we’ll send a one-time reset link.</p><form onSubmit={submit}><div className="field"><label htmlFor="email">Email address</label><input id="email" type="email" autoComplete="email" inputMode="email" required value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com"/></div>{message && <p className="feedback success" role="status">{message}</p>}{error && <p className="feedback error" role="alert">{error}</p>}<button className="button" disabled={busy} aria-busy={busy}>{busy && <span className="button-spinner" aria-hidden="true"/>}{busy ? "Sending link" : "Send reset link"}</button></form></section></main>;
}
