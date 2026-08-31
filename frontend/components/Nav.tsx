"use client";

import Link from "next/link";
import { useState, useSyncExternalStore } from "react";
import { usePathname, useRouter } from "next/navigation";
import { clearToken, getToken, subscribeToAuth } from "@/lib/api";
import { Icon } from "@/components/Icon";

const links = [
  ["/dashboard", "Dashboard", "dashboard"],
  ["/chat", "Assistant", "chat"],
  ["/profile", "Profile", "profile"],
  ["/history", "History", "history"],
] as const;

export function Nav() {
  const pathname = usePathname();
  const router = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);
  const authenticated = useSyncExternalStore(subscribeToAuth, () => Boolean(getToken()), () => false);

  function logout() {
    clearToken();
    setMenuOpen(false);
    router.push("/");
    router.refresh();
  }

  return (
    <header className="site-header">
      <Link href={authenticated ? "/dashboard" : "/"} className="brand" aria-label="Wealth Assistant home">
        <span className="brand-mark" aria-hidden="true"><Icon name="trend" size={21}/></span>
        <span><strong>Wealth</strong><small>AI finance assistant</small></span>
      </Link>
      <button className="menu-button" type="button" aria-label={menuOpen ? "Close navigation" : "Open navigation"} aria-expanded={menuOpen} aria-controls="primary-navigation" onClick={() => setMenuOpen(open => !open)}>
        <Icon name={menuOpen ? "close" : "menu"} size={22}/>
      </button>
      <nav id="primary-navigation" aria-label="Primary navigation" className={menuOpen ? "open" : ""}>
        {authenticated ? links.map(([href, label, icon]) => (
          <Link key={href} href={href} onClick={()=>setMenuOpen(false)} className={pathname === href ? "active" : ""} aria-current={pathname === href ? "page" : undefined}>
            <Icon name={icon}/><span>{label}</span>
          </Link>
        )) : <>
          <Link href="/login" onClick={()=>setMenuOpen(false)}>Log in</Link>
          <Link href="/register" className="nav-cta" onClick={()=>setMenuOpen(false)}>Create account <Icon name="arrow"/></Link>
        </>}
        {authenticated && <button className="nav-logout" type="button" onClick={logout}>Log out</button>}
      </nav>
    </header>
  );
}
