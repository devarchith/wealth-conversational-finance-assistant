import Link from "next/link";

export function LoadingPanel({ label = "Loading your financial workspace" }: { label?: string }) {
  return <div className="status-panel" role="status" aria-live="polite"><span className="spinner" aria-hidden="true"/><div><strong>{label}</strong><p>Bringing your latest information into view.</p></div></div>;
}

export function ErrorPanel({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return <div className="status-panel error-panel" role="alert"><span className="status-symbol" aria-hidden="true">!</span><div><strong>We couldn’t load this view</strong><p>{message}</p>{onRetry && <button className="text-action" type="button" onClick={onRetry}>Try again</button>}</div></div>;
}

export function EmptyPanel({ title, description, href, action }: { title: string; description: string; href?: string; action?: string }) {
  return <div className="empty-panel"><span className="empty-orbit" aria-hidden="true">●</span><h3>{title}</h3><p>{description}</p>{href && action && <Link className="button secondary compact" href={href}>{action}</Link>}</div>;
}
