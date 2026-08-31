import Link from "next/link";

const features = [
  ["01", "See the numbers clearly", "Turn income and expenses into transparent surplus, savings-rate, and emergency-fund metrics."],
  ["02", "Ask in plain language", "Switch between an explainable rule engine and an intent-aware assistant without pretending to know live markets."],
  ["03", "Keep your context private", "Your financial profile and conversation history are scoped to your account, with no bank credentials required."],
];

export default function Home() {
  return <main><section className="container hero"><div><p className="eyebrow">Personal finance, made legible</p><h1>Know where your money can go next.</h1><p className="lede">A calm, conversational workspace for understanding cash flow, building financial resilience, and learning investment fundamentals—without hype or guaranteed-return nonsense.</p><div className="actions"><Link className="button" href="/register">Build your plan</Link><Link className="button secondary" href="/login">Open dashboard</Link></div></div><div className="hero-visual" aria-label="Example monthly overview"><p className="mini-label">Estimated monthly surplus</p><div className="surplus">$1,240</div><div className="bar-row"><span>Essentials</span><div className="bar"><span style={{width:"68%"}} /></div><span>68%</span></div><div className="bar-row"><span>Flexible</span><div className="bar"><span style={{width:"19%"}} /></div><span>19%</span></div><div className="bar-row"><span>Future</span><div className="bar"><span style={{width:"13%"}} /></div><span>13%</span></div><p className="mini-label" style={{marginTop: 46}}>The arithmetic stays deterministic. The explanation stays human.</p></div></section><section className="container features"><div className="section-heading"><h2>Useful before it is impressive.</h2><p>The assistant separates calculations from AI-generated language, labels assumptions, and keeps live-market claims out unless a trusted data source is actually configured.</p></div><div className="feature-grid">{features.map(([n,t,d])=><article className="card feature-card" key={n}><span className="feature-number">{n}</span><h3>{t}</h3><p className="muted">{d}</p></article>)}</div></section></main>;
}

