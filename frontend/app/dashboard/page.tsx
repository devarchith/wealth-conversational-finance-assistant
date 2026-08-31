"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { Protected } from "@/components/Protected";
import { api, formatMoney, formatPercent } from "@/lib/api";
import type { RecommendationSummary } from "@/lib/types";
import { Icon } from "@/components/Icon";
import { EmptyPanel, ErrorPanel, LoadingPanel } from "@/components/StatusPanel";

type History = { items: Array<{id:string; title:string; updated_at:string; last_intent:string|null}>; total:number };
type FinancialProfile = { monthly_income:number; monthly_expenses:number; current_savings:number; monthly_investment:number; risk_tolerance:string; investment_horizon_months:number };
type UserProfile = { preferred_currency:string };

export default function Dashboard() {
  const [summary, setSummary] = useState<RecommendationSummary | null>(null);
  const [financial,setFinancial]=useState<FinancialProfile|null>(null);
  const [currency,setCurrency]=useState("USD");
  const [history,setHistory]=useState<History|null>(null);
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState("");

  const load=useCallback(async()=>{
    setLoading(true); setError("");
    try {
      const [s,f,h,p]=await Promise.all([api<RecommendationSummary>("/recommendations"),api<FinancialProfile>("/financial-profile"),api<History>("/history?page_size=4"),api<UserProfile>("/profile")]);
      setSummary(s);setFinancial(f);setHistory(h);setCurrency(p.preferred_currency);
    } catch(e) { setError(e instanceof Error?e.message:"Unable to load dashboard"); }
    finally { setLoading(false); }
  },[]);
  useEffect(()=>{
    void Promise.all([api<RecommendationSummary>("/recommendations"),api<FinancialProfile>("/financial-profile"),api<History>("/history?page_size=4"),api<UserProfile>("/profile")])
      .then(([s,f,h,p])=>{setSummary(s);setFinancial(f);setHistory(h);setCurrency(p.preferred_currency);})
      .catch(e=>setError(e instanceof Error?e.message:"Unable to load dashboard"))
      .finally(()=>setLoading(false));
  },[]);

  return <Protected><main className="container dashboard-page">
    <div className="page-head dashboard-head"><div><p className="eyebrow">Your financial command center</p><h1>Financial overview</h1><p className="page-subtitle">A clear view of this month, your goals, and what deserves attention next.</p></div><Link className="button" href="/chat"><Icon name="spark"/> Ask Wealth AI</Link></div>
    {loading&&<LoadingPanel label="Calculating your financial overview"/>}
    {!loading&&error&&<ErrorPanel message={error} onRetry={()=>void load()}/>}
    {!loading&&summary&&financial&&<>
      <section className="metrics" aria-label="Primary financial metrics">
        <article className="metric-card"><div className="metric-top"><span className="metric-label">Monthly income</span><span className="metric-icon"><Icon name="trend"/></span></div><div className="metric-value">{formatMoney(financial.monthly_income,currency)}</div><p>Total income reported per month</p></article>
        <article className="metric-card"><div className="metric-top"><span className="metric-label">Monthly expenses</span><span className="metric-icon amber"><Icon name="arrow"/></span></div><div className="metric-value">{formatMoney(financial.monthly_expenses,currency)}</div><p>{formatPercent(summary.expense_ratio)} of monthly income</p></article>
        <article className={`metric-card featured ${summary.monthly_surplus<0?"negative":""}`}><div className="metric-top"><span className="metric-label">Monthly surplus</span><span className="metric-icon"><Icon name="spark"/></span></div><div className="metric-value">{formatMoney(summary.monthly_surplus,currency)}</div><p>{summary.monthly_surplus>=0?"Available after reported expenses":"Expenses currently exceed income"}</p></article>
        <article className="metric-card"><div className="metric-top"><span className="metric-label">Savings rate</span><span className="metric-icon"><Icon name="target"/></span></div><div className="metric-value">{formatPercent(summary.savings_rate)}</div><p>Based on income and surplus</p></article>
      </section>

      <section className="dashboard-grid">
        <div className="dashboard-primary">
          <article className="card recommendation-card"><div className="card-heading"><div><p className="eyebrow">Personalized guidance</p><h2>Recommended next steps</h2></div><span className="insight-badge"><Icon name="spark"/> Explainable</span></div>{summary.recommendations.length?summary.recommendations.slice(0,4).map((r,index)=><div className="recommendation" key={`${r.category}-${r.title}`}><span className={`priority-dot ${r.priority}`} aria-label={`${r.priority} priority`}/><div><div className="recommendation-title"><h3>{r.title}</h3><span className={`pill ${r.priority}`}>{r.priority}</span></div><p>{r.explanation}</p></div><span className="recommendation-number" aria-hidden="true">0{index+1}</span></div>):<EmptyPanel title="You’re all caught up" description="Add more detail to your profile to receive tailored recommendations." href="/profile" action="Review profile"/>}</article>

          <article className="card goals-card"><div className="card-heading"><div><p className="eyebrow">Progress that matters</p><h2>Financial goals</h2></div><Link className="text-action" href="/profile">Manage goals <Icon name="arrow"/></Link></div>{summary.goal_progress.length?<div className="goal-list">{summary.goal_progress.map(goal=><div className="goal-row" key={goal.id}><div className="goal-row-head"><div><span className="goal-icon"><Icon name="target"/></span><strong>{goal.name}</strong></div><strong>{formatPercent(goal.progress)}</strong></div><div className="progress" aria-label={`${goal.name} ${Math.round(goal.progress*100)} percent complete`}><span style={{width:`${Math.min(100,goal.progress*100)}%`}}/></div><small>{formatMoney(goal.remaining,currency)} remaining</small></div>)}</div>:<EmptyPanel title="No goals added yet" description="Give your savings a destination—add a target and track progress here." href="/profile" action="Add your first goal"/>}</article>
        </div>

        <aside className="dashboard-side">
          <article className="card health-card"><p className="eyebrow">Financial readiness</p><div className="health-row"><div className="reserve-ring" style={{background:`radial-gradient(circle at center, white 52%, transparent 54%), conic-gradient(var(--green) 0 ${summary.emergency_fund_target>0?Math.round(Math.min(100,(financial.current_savings/summary.emergency_fund_target)*100)):0}%, var(--paper-deep) 0)`}}><span>{summary.emergency_fund_target>0?Math.round(Math.min(100,(financial.current_savings/summary.emergency_fund_target)*100)):0}%</span></div><div><h2>Emergency reserve</h2><p>{formatMoney(financial.current_savings,currency)} of {formatMoney(summary.emergency_fund_target,currency)}</p></div></div><div className="health-detail"><span>Remaining gap</span><strong>{formatMoney(summary.emergency_fund_gap,currency)}</strong></div><div className="health-detail"><span>Risk profile</span><strong className="capitalize">{summary.risk_profile}</strong></div><Link href="/profile" className="button secondary compact">Review financial profile</Link></article>

          <article className="card recent-card"><div className="card-heading"><div><p className="eyebrow">Continue the conversation</p><h2>Recent questions</h2></div><Icon name="chat"/></div>{history?.items.length?<div className="recent-list">{history.items.map(item=><Link href="/history" className="recent-row" key={item.id}><div><strong>{item.title}</strong><span>{item.last_intent?.replaceAll("_"," ")??"New conversation"}</span></div><Icon name="chevron"/></Link>)}</div>:<EmptyPanel title="No conversations yet" description="Ask one focused finance question and your history will appear here." href="/chat" action="Start a conversation"/>}{Boolean(history?.items.length)&&<Link href="/history" className="text-action view-all">View all conversations <Icon name="arrow"/></Link>}</article>
        </aside>
      </section>
    </>}
  </main></Protected>;
}
