import Link from "next/link";
import { Icon } from "@/components/Icon";

export default function NotFound(){
  return <main className="container fatal-state"><span className="form-icon" aria-hidden="true"><Icon name="target"/></span><p className="eyebrow">Page not found</p><h1>This path doesn’t add up.</h1><p>The page may have moved, or the address may be incomplete.</p><Link className="button" href="/">Return home <Icon name="arrow"/></Link></main>;
}
