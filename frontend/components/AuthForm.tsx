"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api, setToken } from "@/lib/api";
import type { User } from "@/lib/types";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  const registering = mode === "register";
  async function submit(event: FormEvent) {
    event.preventDefault(); setError(""); setBusy(true);
    try {
      const result = await api<{ access_token: string; user: User }>(`/auth/${registering ? "register" : "login"}`, { method: "POST", body: JSON.stringify({ email, password }) });
      setToken(result.access_token); router.push("/dashboard"); router.refresh();
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Unable to continue"); }
    finally { setBusy(false); }
  }
  return <main className="form-shell"><p className="eyebrow">Private by design</p><h1>{registering ? "Start with your real numbers." : "Welcome back."}</h1><div className="form-card"><form onSubmit={submit}><div className="field"><label htmlFor="email">Email</label><input id="email" type="email" autoComplete="email" required value={email} onChange={e=>setEmail(e.target.value)} /></div><div className="field"><label htmlFor="password">Password</label><input id="password" type="password" minLength={registering ? 10 : undefined} autoComplete={registering ? "new-password" : "current-password"} required value={password} onChange={e=>setPassword(e.target.value)} /><small className="muted">{registering ? "At least 10 characters, including a letter and number." : <Link href="/forgot-password">Forgot password?</Link>}</small></div>{error && <p className="error" role="alert">{error}</p>}<button className="button" disabled={busy}>{busy ? "Working…" : registering ? "Create account" : "Log in"}</button></form><p className="muted" style={{margin:"20px 0 0"}}>{registering ? <>Already registered? <Link href="/login">Log in</Link></> : <>New here? <Link href="/register">Create an account</Link></>}</p></div></main>;
}

