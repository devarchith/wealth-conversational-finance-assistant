"use client";

import { Icon } from "@/components/Icon";

export default function ErrorPage({retry}:{error:Error&{digest?:string};retry:()=>void}){
  return <main className="container fatal-state"><span className="danger-symbol" aria-hidden="true">!</span><p className="eyebrow">Something interrupted this view</p><h1>Let’s try that again.</h1><p>The rest of your financial workspace is safe. Retry this page or return through the main navigation.</p><button className="button" type="button" onClick={retry}>Retry page <Icon name="arrow"/></button></main>;
}
