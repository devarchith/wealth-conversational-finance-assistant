"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api, setToken } from "@/lib/api";
import type { User } from "@/lib/types";
import { Icon } from "@/components/Icon";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  const registering = mode === "register";
  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    if (registering && (!/[A-Za-z]/.test(password) || !/\d/.test(password))) {
      setError("Use at least one letter and one number in your password.");
      return;
    }
    setBusy(true);
    try {
      const result = await api<{ access_token: string; user: User }>(`/auth/${registering ? "register" : "login"}`, { method: "POST", body: JSON.stringify({ email, password }) });
      setToken(result.access_token); router.push("/dashboard"); router.refresh();
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Unable to continue"); }
    finally { setBusy(false); }
  }
  return <main className="auth-shell">
    <section className="auth-intro" aria-label="Product summary">
      <p className="eyebrow">Private by design</p>
      <h1>{registering ? "Start with clarity, not complexity." : "Welcome back."}</h1>
      <p className="lede">Your financial picture, explainable recommendations, and two ways to ask questions—all in one calm workspace.</p>
      <div className="auth-proof"><span><Icon name="trend"/> Deterministic metrics</span><span><Icon name="spark"/> AI-assisted explanations</span><span><Icon name="target"/> Goal-aware planning</span></div>
    </section>
    <section className="form-card auth-card">
      <div className="form-heading"><span className="form-icon" aria-hidden="true"><Icon name={registering ? "spark" : "profile"}/></span><div><p className="eyebrow">{registering ? "Create your workspace" : "Secure account access"}</p><h2>{registering ? "Create account" : "Log in"}</h2></div></div>
      <form onSubmit={submit} noValidate>
        <div className="field"><label htmlFor="email">Email address</label><input id="email" type="email" autoComplete="email" inputMode="email" required aria-describedby="email-help" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com"/><small id="email-help">Used only to secure and identify your workspace.</small></div>
        <div className="field"><div className="label-row"><label htmlFor="password">Password</label>{!registering && <Link className="text-link" href="/forgot-password">Forgot password?</Link>}</div><input id="password" type="password" minLength={registering ? 10 : undefined} autoComplete={registering ? "new-password" : "current-password"} required aria-describedby={registering ? "password-help" : undefined} value={password} onChange={e=>setPassword(e.target.value)} placeholder={registering ? "10+ characters" : "Enter your password"}/>{registering && <small id="password-help">At least 10 characters, including a letter and number.</small>}</div>
        {error && <p className="feedback error" role="alert">{error}</p>}
        <button className="button" disabled={busy} aria-busy={busy}>{busy && <span className="button-spinner" aria-hidden="true"/>}{busy ? "Please wait" : registering ? "Create account" : "Log in"}</button>
      </form>
      <p className="form-switch">{registering ? <>Already registered? <Link href="/login">Log in</Link></> : <>New to Wealth? <Link href="/register">Create an account</Link></>}</p>
    </section>
  </main>;
}
