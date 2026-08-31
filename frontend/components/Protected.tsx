"use client";

import { useEffect, useSyncExternalStore } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/api";

export function Protected({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const authenticated = useSyncExternalStore(() => () => undefined, () => Boolean(getToken()), () => false);
  useEffect(() => {
    if (!authenticated) router.replace("/login");
  }, [authenticated, router]);
  return authenticated ? children : <main className="centered session-check" role="status"><span className="spinner" aria-hidden="true"/><div><strong>Checking your session</strong><p>Opening your private financial workspace…</p></div></main>;
}
