import type { Metadata } from "next";
import "./globals.css";
import { Nav } from "@/components/Nav";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"),
  title: { default: "Wealth · AI-powered personal finance assistant", template: "%s · Wealth" },
  description: "Understand cash flow, goals, risk, and financial fundamentals with explainable metrics and two conversational assistant modes.",
  openGraph: {
    title: "Wealth · AI-powered personal finance assistant",
    description: "Understand cash flow, goals, risk, and financial fundamentals with explainable metrics and conversational guidance.",
    images: [{url:"/og.png",width:1731,height:909,alt:"Wealth — AI-powered personal finance assistant"}],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Wealth · AI-powered personal finance assistant",
    description: "Explainable personal-finance metrics and conversational guidance.",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><a className="skip-link" href="#main-content">Skip to main content</a><Nav /><div id="main-content">{children}</div><footer><span className="footer-brand">Wealth <small>AI finance assistant</small></span><span>Educational information — not professional financial advice.</span></footer></body></html>;
}
