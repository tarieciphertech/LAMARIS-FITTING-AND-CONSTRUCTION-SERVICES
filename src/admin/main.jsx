import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Building2, Home, ImagePlus, LayoutDashboard, LogOut, MessageCircle, Plus, Settings, Tag, Users } from 'lucide-react'
import '../styles.css'
import './admin.css'

const stats = [
  ['Active listings', '8', 'Manage properties'],
  ['Featured deals', '3', 'Promoted listings'],
  ['New enquiries', '12', 'Needs follow-up'],
  ['Sold / archived', '6', 'Listing history'],
]

function Admin() {
  const [section, setSection] = useState('Dashboard')
  const nav = [
    ['Dashboard', LayoutDashboard], ['Properties', Home], ['Enquiries', MessageCircle], ['Blog', Tag], ['Media', ImagePlus], ['Team', Users], ['Settings', Settings],
  ]
  return <div className="admin-shell">
    <aside className="admin-sidebar">
      <div className="admin-brand"><span className="brand-mark"><Building2 size={20}/></span><span><strong>LAMARIS</strong><small>ADMIN</small></span></div>
      <nav>{nav.map(([label, Icon]) => <button className={section === label ? 'active' : ''} onClick={() => setSection(label)} key={label}><Icon size={18}/>{label}</button>)}</nav>
      <a className="admin-exit" href="/"><LogOut size={17}/> View website</a>
    </aside>
    <main className="admin-main">
      <header className="admin-header"><div><span className="kicker">LAMARIS MANAGEMENT</span><h1>{section}</h1></div><button className="button primary"><Plus size={17}/> Add Property</button></header>
      {section === 'Dashboard' ? <Dashboard/> : <Placeholder section={section}/>} 
    </main>
  </div>
}

function Dashboard(){return <>
  <div className="admin-stats">{stats.map(([label,value,sub])=><div className="stat" key={label}><small>{label}</small><strong>{value}</strong><span>{sub}</span></div>)}</div>
  <div className="admin-columns"><section className="admin-panel"><div className="panel-heading"><div><strong>Recent enquiries</strong><small>Latest customer conversations</small></div><a href="#">View all</a></div><div className="enquiry"><MessageCircle/><div><strong>Property enquiry</strong><small>Buyer interested in a residential property</small></div><span>Today</span></div><div className="enquiry"><MessageCircle/><div><strong>Construction enquiry</strong><small>Renovation and ceiling project</small></div><span>Yesterday</span></div><div className="enquiry"><MessageCircle/><div><strong>Stand enquiry</strong><small>Looking for a residential stand</small></div><span>2 days ago</span></div></section>
  <section className="admin-panel"><div className="panel-heading"><div><strong>Listing status</strong><small>Keep availability current</small></div></div><div className="status-row"><span>Available</span><strong>8</strong></div><div className="status-row"><span>Featured</span><strong>3</strong></div><div className="status-row"><span>Sold</span><strong>6</strong></div><div className="status-row"><span>Draft</span><strong>2</strong></div></section></div>
  <section className="admin-panel workflow"><div><strong>Property publishing workflow</strong><p>Add the property details, upload photos, set price and availability, then publish. The public website will use these records instead of hardcoded listings once the backend is connected.</p></div><button className="button primary"><Plus size={17}/> Create first listing</button></section>
</>}

function Placeholder({section}){return <div className="admin-empty"><div className="service-icon"><LayoutDashboard/></div><h2>{section} management</h2><p>This admin module is scaffolded and ready for the database/API layer. The next implementation step is connecting it to authenticated property and enquiry data.</p></div>}

createRoot(document.getElementById('admin-root')).render(<Admin />)
