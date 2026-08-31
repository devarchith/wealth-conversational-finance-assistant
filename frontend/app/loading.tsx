export default function Loading(){
  return <main className="container route-loading" role="status" aria-label="Loading page"><div className="skeleton heading-skeleton"/><div className="skeleton-grid">{Array.from({length:4},(_,index)=><div className="skeleton card-skeleton" key={index}/>)}</div></main>;
}
