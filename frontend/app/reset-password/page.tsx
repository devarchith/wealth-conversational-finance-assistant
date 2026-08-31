"use client";

import { FormEvent, Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { api } from "@/lib/api";
import { Icon } from "@/components/Icon";

function ResetPasswordForm() {
  const params = useSearchParams(); const token=params.get("token"); const [password,setPassword]=useState(""); const [message,setMessage]=useState(""); const [error,setError]=useState(""); const [busy,setBusy]=useState(false);
  async function submit(e:FormEvent){e.preventDefault();setError("");setMessage("");if(!token){setError("This reset link is incomplete. Request a new link to continue.");return;}if(!/[A-Za-z]/.test(password)||!/\d/.test(password)){setError("Use at least one letter and one number in your password.");return;}setBusy(true);try{const result=await api<{message:string}>("/auth/password-reset/confirm",{method:"POST",body:JSON.stringify({token,new_password:password})});setMessage(result.message);}catch(cause){setError(cause instanceof Error?cause.message:"Unable to reset password");}finally{setBusy(false);}}
  return <main className="narrow-page"><div className="back-link"><Link href="/login">← Back to log in</Link></div><section className="form-card recovery-card"><span className="form-icon" aria-hidden="true"><Icon name="profile"/></span><p className="eyebrow">One-time link</p><h1>Choose a new password</h1><p className="muted">Create a password you don’t use elsewhere.</p><form onSubmit={submit}><div className="field"><label htmlFor="password">New password</label><input id="password" type="password" autoComplete="new-password" minLength={10} required aria-describedby="password-help" value={password} onChange={e=>setPassword(e.target.value)} placeholder="10+ characters"/><small id="password-help">At least 10 characters, including a letter and number.</small></div>{message&&<p className="feedback success" role="status">{message} <Link href="/login">Log in now.</Link></p>}{error&&<p className="feedback error" role="alert">{error}</p>}<button className="button" disabled={busy} aria-busy={busy}>{busy&&<span className="button-spinner" aria-hidden="true"/>}{busy?"Updating password":"Update password"}</button></form></section></main>;
}

export default function ResetPassword() {
  return <Suspense fallback={<main className="centered"><span className="spinner" aria-hidden="true"/><p>Preparing password reset…</p></main>}><ResetPasswordForm /></Suspense>;
}
