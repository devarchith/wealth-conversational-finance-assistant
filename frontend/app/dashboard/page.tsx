"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Protected } from "@/components/Protected";
import { api, formatMoney, formatPercent } from "@/lib/api";
import type { RecommendationSummary } from "@/lib/types";

type History = { items: Array<{id:string; title:string; updated_at:string; last_intent:string|null}>; total:number };

export default function Dashboard() {
  const [summary, setSummary] = useState<RecommendationSummary | null>(null); const [history,setHistory]=useState<History|null>(null); const [error,setError]=useState("");
  useEffect(()=>{Promise.all([api<RecommendationSummary>("/recommendations"),api<History>("/history?page_size=4")]).then(([s,h])=>{setSummary(s);setHistory(h);}).catch(e=>setError(e instanceof Error?e.message:"Unable to load dashboard"));},[]);
  return <Protected><main className="container"><div className="page-head"><div><p className="eyebrow">Your monthly picture</p><h1>Financial overview</h1></div><Link className="button" href="/chat">Ask the assistant</Link></div>{error&&<p className="error">{error}</p>}{!summary?<div className="card">Loading your metrics…</div>:<><section className="grid metrics" aria-label="Financial metrics"><div className="card"><span className="metric-label">Monthly surplus</span><div className="metric-value">{formatMoney(summary.monthly_surplus)}</div></div><div className="card"><span className="metric-label">Savings rate</span><div className="metric-value">{formatPercent(summary.savings_rate)}</div></div><div className="card"><span className="metric-label">Expense ratio</span><div className="metric-value">{formatPercent(summary.expense_ratio)}</div></div><div className="card"><span className="metric-label">Reserve gap</span><div className="metric-value">{formatMoney(summary.emergency_fund_gap)}</div></div></section><section className="grid dashboard-grid"><div className="card"><span className="eyebrow">Next best actions</span><h2 style={{fontSize:38,marginTop:12}}>Recommendations</h2>{summary.recommendations.map(r=><article className="recommendation" key={`${r.category}-${r.title}`}><span className="pill">{r.priority} priority</span><h3 style={{margin:"10px 0 5px"}}>{r.title}</h3><p className="muted">{r.explanation}</p></article>)}</div><div className="grid"><div className="card"><span className="metric-label">Risk profile</span><div className="metric-value" style={{textTransform:"capitalize"}}>{summary.risk_profile}</div><p className="muted">A self-reported tolerance label—not a promise that a portfolio is suitable.</p><Link href="/profile" className="button secondary">Review profile</Link></div><div className="card"><span className="eyebrow">Recent questions</span>{history?.items.length?history.items.map(item=><div className="recommendation" key={item.id}><h3>{item.title}</h3><span className="muted">{item.last_intent?.replaceAll("_"," ")??"New conversation"}</span></div>):<p className="muted" style={{marginTop:18}}>No conversations yet. Ask one focused finance question.</p>}<Link href="/history" className="button secondary">View history</Link></div></div></section></>}</main></Protected>;
}

