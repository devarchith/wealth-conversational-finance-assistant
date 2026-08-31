"use client";

import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import { Protected } from "@/components/Protected";
import { api } from "@/lib/api";
import type { ChatReply, Entity } from "@/lib/types";
import { Icon } from "@/components/Icon";

type Message={role:"user"|"assistant";content:string;intent?:string;engine?:string;entities?:Entity[];confidence?:number};

export default function ChatPage(){
 const [engine,setEngine]=useState<"rule-based"|"ai">("ai");const [input,setInput]=useState("");const [messages,setMessages]=useState<Message[]>([]);const [conversation,setConversation]=useState<string|null>(null);const [busy,setBusy]=useState(false);const [error,setError]=useState("");const endRef=useRef<HTMLDivElement>(null);
 useEffect(()=>{endRef.current?.scrollIntoView?.({behavior:"smooth",block:"end"});},[messages,busy]);
 async function submit(e:FormEvent){e.preventDefault();const question=input.trim();if(!question||busy)return;setMessages(current=>[...current,{role:"user",content:question}]);setInput("");setBusy(true);setError("");try{const reply=await api<ChatReply>(`/chat/${engine}`,{method:"POST",body:JSON.stringify({message:question,conversation_id:conversation})});setConversation(reply.conversation_id);setMessages(current=>[...current,{role:"assistant",content:reply.response,intent:reply.intent,engine:reply.engine,entities:reply.entities,confidence:reply.confidence}]);}catch(cause){setError(cause instanceof Error?cause.message:"The assistant could not respond");}finally{setBusy(false);}}
 function onKeyDown(e:KeyboardEvent<HTMLTextAreaElement>){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();e.currentTarget.form?.requestSubmit();}}
 function newConversation(){setMessages([]);setConversation(null);setError("");setInput("");}
 const suggestions=["How healthy is my monthly cash flow?","How large should my emergency fund be?","Help me plan for a financial goal."];
 return <Protected><main className="chat-layout">
  <aside className="chat-side">
    <div><p className="eyebrow">Choose your assistant</p><h1>Wealth AI</h1><p>Ask about your cash flow, savings, goals, risk, or investing fundamentals.</p></div>
    <div className="engine-switch" role="radiogroup" aria-label="Assistant engine">
      <button type="button" role="radio" aria-checked={engine==="ai"} className={engine==="ai"?"selected":""} onClick={()=>setEngine("ai")}><span className="engine-icon ai"><Icon name="spark"/></span><span><strong>AI Assistant</strong><small>Intent-aware guidance</small></span><span className="selected-check" aria-hidden="true">✓</span></button>
      <button type="button" role="radio" aria-checked={engine==="rule-based"} className={engine==="rule-based"?"selected":""} onClick={()=>setEngine("rule-based")}><span className="engine-icon"><Icon name="trend"/></span><span><strong>Rule-Based</strong><small>Predictable and offline</small></span><span className="selected-check" aria-hidden="true">✓</span></button>
    </div>
    <div className="engine-note"><span className="status-dot" aria-hidden="true"/><span><strong>{engine==="ai"?"AI mode active":"Rule engine active"}</strong><small>{engine==="ai"?"Uses the configured safe provider":"Uses deterministic intent matching"}</small></span></div>
    {messages.length>0&&<button className="button secondary compact new-chat" type="button" onClick={newConversation}>+ New conversation</button>}
    <p className="privacy-note">Your history stays private to your account. Never share account numbers or passwords.</p>
  </aside>
  <section className="chat-main" aria-label="Finance assistant conversation">
    <header className="chat-header"><div><span className="chat-avatar"><Icon name={engine==="ai"?"spark":"trend"}/></span><div><strong>{engine==="ai"?"AI Assistant":"Rule-Based Assistant"}</strong><span><i/> Ready to help</span></div></div><span className="engine-badge">{engine==="ai"?"Intent aware":"Deterministic"}</span></header>
    <div className="messages" aria-live="polite" aria-busy={busy}>
      {messages.length===0&&<div className="chat-empty"><span className="chat-empty-icon" aria-hidden="true"><Icon name="spark" size={28}/></span><p className="eyebrow">Your finances, explained</p><h2>What would you like to understand?</h2><p>Ask a focused question. I’ll connect the answer to the financial profile you’ve provided and clearly label assumptions.</p><div className="prompt-list" aria-label="Suggested questions">{suggestions.map(s=><button type="button" key={s} onClick={()=>setInput(s)}><Icon name="chat"/><span>{s}</span><Icon name="arrow"/></button>)}</div></div>}
      {messages.map((m,index)=><article className={`message-row ${m.role}`} key={index}><span className="message-avatar" aria-hidden="true">{m.role==="user"?"You":<Icon name="spark"/>}</span><div className={`message ${m.role}`}><div className="message-label">{m.role==="user"?"You":m.engine?.includes("rule")?"Rule-Based Assistant":"AI Assistant"}</div><p>{m.content}</p>{m.role==="assistant"&&<details className="message-insights"><summary>Why this answer <Icon name="chevron"/></summary><div className="meta"><span>Intent <strong>{m.intent?.replaceAll("_"," ")}</strong></span><span>Confidence <strong>{Math.round((m.confidence??0)*100)}%</strong></span>{Boolean(m.entities?.length)&&<span>Recognized <strong>{m.entities?.map(e=>`${e.type}: ${e.value}`).join(", ")}</strong></span>}</div></details>}</div></article>)}
      {busy&&<article className="message-row assistant"><span className="message-avatar" aria-hidden="true"><Icon name="spark"/></span><div className="message assistant typing"><span/><span/><span/><em>{engine==="ai"?"Connecting the question to your profile":"Matching finance concepts"}</em></div></article>}
      {error&&<div className="chat-error" role="alert"><span aria-hidden="true">!</span><div><strong>That response didn’t come through</strong><p>{error}</p></div></div>}
      <div ref={endRef}/>
    </div>
    <div className="composer"><form onSubmit={submit}><label className="sr-only" htmlFor="finance-question">Your finance question</label><textarea id="finance-question" value={input} onChange={e=>setInput(e.target.value)} onKeyDown={onKeyDown} maxLength={2000} rows={1} placeholder="Ask about cash flow, savings, risk, or goals…"/><button className="send-button" aria-label="Send question" disabled={busy||!input.trim()}><Icon name="send"/></button></form><div className="composer-meta"><span>Enter to send · Shift + Enter for a new line</span><span>Educational guidance · No trades or live prices</span></div></div>
  </section>
 </main></Protected>;
}
