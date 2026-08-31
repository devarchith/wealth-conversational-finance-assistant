"use client";

import { FormEvent, Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api } from "@/lib/api";

function ResetPasswordForm() {
  const params = useSearchParams(); const [password,setPassword]=useState(""); const [message,setMessage]=useState(""); const [error,setError]=useState("");
  async function submit(e:FormEvent){e.preventDefault();setError("");try{const result=await api<{message:string}>("/auth/password-reset/confirm",{method:"POST",body:JSON.stringify({token:params.get("token"),new_password:password})});setMessage(result.message);}catch(cause){setError(cause instanceof Error?cause.message:"Unable to reset password");}}
  return <main className="form-shell"><p className="eyebrow">One-time link</p><h1>Choose a new password.</h1><div className="form-card"><form onSubmit={submit}><div className="field"><label htmlFor="password">New password</label><input id="password" type="password" minLength={10} required value={password} onChange={e=>setPassword(e.target.value)} /></div>{message&&<p className="success">{message}</p>}{error&&<p className="error">{error}</p>}<button className="button">Update password</button></form></div></main>;
}

export default function ResetPassword() {
  return <Suspense fallback={<main className="centered"><p>Preparing password reset…</p></main>}><ResetPasswordForm /></Suspense>;
}
