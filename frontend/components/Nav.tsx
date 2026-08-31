"use client";

import Link from "next/link";
import { useSyncExternalStore } from "react";
import { usePathname, useRouter } from "next/navigation";
import { clearToken, getToken } from "@/lib/api";

const links = [
  ["/dashboard", "Dashboard"],
  ["/chat", "Assistant"],
  ["/profile", "Profile"],
  ["/history", "History"],
];

export function Nav() {
  const pathname = usePathname();
  const router = useRouter();
  const authenticated = useSyncExternalStore(() => () => undefined, () => Boolean(getToken()), () => false);
  return (
    <header className="site-header">
      <Link href="/" className="brand" aria-label="Wealth Assistant home"><span className="brand-mark">W</span><span>Wealth Assistant</span></Link>
      <nav aria-label="Primary navigation">
        {authenticated ? links.map(([href, label]) => <Link key={href} href={href} className={pathname === href ? "active" : ""}>{label}</Link>) : <><Link href="/login">Log in</Link><Link href="/register" className="nav-cta">Create account</Link></>}
        {authenticated && <button className="link-button" onClick={() => { clearToken(); router.push("/"); router.refresh(); }}>Log out</button>}
      </nav>
    </header>
  );
}
