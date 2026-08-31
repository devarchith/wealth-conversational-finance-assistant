"use client";

import { useCallback, useEffect, useState } from "react";
import { Protected } from "@/components/Protected";
import { api } from "@/lib/api";

type Item={id:string;title:string;created_at:string;updated_at:string;last_engine:string|null;last_intent:string|null};
type Page={items:Item[];page:number;page_size:number;total:number};
type Detail={conversation:Item;messages:Array<{id:string;role:string;content:string;created_at:string;intent:string|null;engine:string}>};

export default function HistoryPage(){
 const [page,setPage]=useState<Page|null>(null);const [detail,setDetail]=useState<Detail|null>(null);const [error,setError]=useState("");
 const load=useCallback(()=>api<Page>("/history").then(setPage).catch(e=>setError(e instanceof Error?e.message:"Unable to load history")),[]);
 useEffect(()=>{load();},[load]);
 async function remove(id:string){if(!window.confirm("Delete this conversation permanently?"))return;try{await api(`/history/${id}`,{method:"DELETE"});setDetail(null);await load();}catch(cause){setError(cause instanceof Error?cause.message:"Unable to delete");}}
 async function inspect(id:string){try{setDetail(await api<Detail>(`/history/${id}`));}catch(cause){setError(cause instanceof Error?cause.message:"Unable to open conversation");}}
 return <Protected><main className="container"><div className="page-head"><div><p className="eyebrow">Private to your account</p><h1>Conversation history</h1></div><p className="lede">Revisit the reasoning, not just the final answer.</p></div>{error&&<p className="error">{error}</p>}<section className="history-list">{!page?<div className="card">Loading…</div>:page.items.length===0?<div className="card"><h3>No conversations yet</h3><p className="muted">Your finance questions will appear here after you use the assistant.</p></div>:page.items.map(item=><article className="card history-row" key={item.id}><button className="link-button" style={{textAlign:"left"}} onClick={()=>inspect(item.id)}><h3>{item.title}</h3><span className="muted">{item.last_engine??"new"} · {item.last_intent?.replaceAll("_"," ")??"no intent"} · {new Date(item.updated_at).toLocaleString()}</span></button><button className="button danger" onClick={()=>remove(item.id)}>Delete</button></article>)}</section>{detail&&<div className="form-card" style={{position:"fixed",inset:"12% max(20px,calc((100vw - 760px)/2))",overflow:"auto",zIndex:30}}><button className="link-button" onClick={()=>setDetail(null)} style={{float:"right"}}>Close</button><p className="eyebrow">Conversation detail</p><h2 style={{fontSize:38}}>{detail.conversation.title}</h2>{detail.messages.map(message=><article className={`message ${message.role}`} key={message.id}><div>{message.content}</div>{message.intent&&<div className="meta"><span>{message.engine}</span><span>{message.intent}</span></div>}</article>)}</div>}</main></Protected>;
}

