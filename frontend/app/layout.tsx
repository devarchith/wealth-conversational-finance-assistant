import type { Metadata } from "next";
import "./globals.css";
import { Nav } from "@/components/Nav";

export const metadata: Metadata = {
  title: { default: "Wealth Assistant", template: "%s · Wealth Assistant" },
  description: "Private, explainable tools for budgeting, saving, and financial education.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><Nav />{children}<footer><span>Wealth Assistant</span><span>Educational information — not professional financial advice.</span></footer></body></html>;
}
